from datetime import datetime, timedelta
from email.utils import format_datetime
from typing import Annotated, TypeVar
from uuid import UUID

import content_types
from lxml.etree import CDATA
from pydantic import (
    AfterValidator,
    AwareDatetime,
    BeforeValidator,
    HttpUrl,
    PlainSerializer,
    StringConstraints,
)
from pydantic_xml import BaseXmlModel, XmlFieldSerializer
from pydantic_xml.element import XmlElementWriter


def _bool_to_yes_no(value: bool | None) -> str:
    return "yes" if value else "no"


def _bool_to_yes(value: bool | None) -> str | None:
    return "yes" if value else None


def _bool_to_true_false(value: bool | None) -> str:
    return "true" if value else "false"


def _timedelta_to_seconds(value: timedelta | None) -> str | None:
    return None if value is None else round(value.total_seconds())


def _convert_timedelta(value: timedelta | int | None) -> timedelta | None:
    if isinstance(value, timedelta):
        return value
    elif isinstance(value, int):
        return timedelta(seconds=value)
    else:
        return value


def _convert_uuid(value: UUID | str | None) -> UUID | None:
    if isinstance(value, UUID):
        return value
    elif isinstance(value, str):
        return UUID(value)
    else:
        return value


def _timedelta_to_npt(value: timedelta | None) -> str | None:
    """Format a timedelta as a Normal Play Time (HH:MM:SS.mmm)."""
    if value is None:
        return None

    total_seconds = int(value.total_seconds())

    hours, remainder = divmod(total_seconds, 3_600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = value.microseconds // 1_000

    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def _datetime_to_rfc2822_string(value: datetime | None) -> str | None:
    return None if value is None else format_datetime(value)


def _validate_media_type(media_type: str | None) -> str:
    if (
        media_type
        and media_type not in content_types.EXTENSION_TO_CONTENT_TYPE.values()
    ):
        raise ValueError(f"{media_type} not a recognized media type")
    return media_type


def _string_to_cdata(
    _: BaseXmlModel, element: XmlElementWriter, value: str | None, field_name: str
) -> None:
    if value:
        sub_element = element.make_element(tag=field_name, nsmap=None)
        # noinspection PyTypeChecker
        sub_element.set_text(CDATA(value))
        element.append_element(sub_element)


def _check_byte_size(max_size: int):
    def wrapper(value: str | None) -> str | None:
        actual_size = len(value.encode()) if value else 0
        if actual_size > max_size:
            raise ValueError(
                f"String size of {actual_size} bytes exceeds maximum of {max_size} bytes"
            )
        return value

    return wrapper


def _check_check_positive_timedelta(value: timedelta | None) -> timedelta | None:
    if value is not None and value < timedelta():
        raise ValueError(f"Duration must be positive: {value}")
    return value


def _check_uuid_v5(value: UUID | None):
    if value is not None and value.version != 5:
        raise ValueError(
            f"UUID version 5 expected [version={value.version}, value={value}]"
        )
    return value


_BoolType = TypeVar("_BoolType", bool, bool | None, default=bool)
_StringType = TypeVar("_StringType", str, str | None, default=str)
_DurationType = TypeVar(
    "_DurationType", timedelta | int, timedelta | int | None, default=timedelta | int
)
_UUIDv5Type = TypeVar("_UUIDv5Type", UUID | str, UUID | str, default=UUID | str)

URL = Annotated[str, HttpUrl]
YesNoBool = Annotated[_BoolType, PlainSerializer(_bool_to_yes_no)]
YesBool = Annotated[_BoolType, PlainSerializer(_bool_to_yes)]
MediaType = Annotated[_StringType, AfterValidator(_validate_media_type)]
CData = Annotated[
    _StringType,
    XmlFieldSerializer(_string_to_cdata),
    AfterValidator(_check_byte_size(max_size=4000)),
]
DurationInSeconds = Annotated[
    _DurationType,
    BeforeValidator(_convert_timedelta),
    AfterValidator(_check_check_positive_timedelta),
    PlainSerializer(_timedelta_to_seconds),
]
DateTime = Annotated[
    datetime, AwareDatetime, PlainSerializer(_datetime_to_rfc2822_string)
]
Duration = Annotated[
    _DurationType,
    BeforeValidator(_convert_timedelta),
    AfterValidator(_check_check_positive_timedelta),
    PlainSerializer(_timedelta_to_npt),
]
Language = Annotated[
    _StringType, StringConstraints(pattern=r"^[a-z]{2,3}(?:-[a-z]{2})?$", to_lower=True)
]
UUIDv5 = Annotated[
    _UUIDv5Type,
    BeforeValidator(_convert_uuid),
    # can't use pydantic.types.UuidVersion(5) because it doesn't support nullable types
    AfterValidator(_check_uuid_v5),
]
