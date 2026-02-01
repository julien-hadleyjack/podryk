from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError
from pydantic_xml import element
from syrupy import SnapshotAssertion

from podryk.models.field_types import (
    CData,
    DateTime,
    Duration,
    DurationInSeconds,
    Language,
    MediaType,
    UUIDv5,
    YesBool,
    YesNoBool,
)
from podryk.models.xml_model import XmlModel

from .utils.xml_util import to_xml


class TestYesNoBool:
    class Model(XmlModel, tag="yes-no"):
        value: YesNoBool = element()

    class OptionalModel(XmlModel, tag="yes-no"):
        value: YesNoBool[bool | None] = element()

    def test_true(self, snapshot: SnapshotAssertion):
        model = self.Model(value=True)
        assert to_xml(model) == snapshot

    def test_false(self, snapshot: SnapshotAssertion):
        model = self.Model(value=False)
        assert to_xml(model) == snapshot

    def test_optional(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=True)
        assert to_xml(model) == snapshot

    def test_none(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=None)
        assert to_xml(model) == snapshot


class TestYesBool:
    class Model(XmlModel, tag="yes"):
        value: YesBool = element()

    class OptionalModel(XmlModel, tag="yes"):
        value: YesBool[bool | None] = element()

    def test_true(self, snapshot: SnapshotAssertion):
        model = self.Model(value=True)
        assert to_xml(model) == snapshot

    def test_false(self, snapshot: SnapshotAssertion):
        model = self.Model(value=False)
        assert to_xml(model) == snapshot

    def test_optional(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=True)
        assert to_xml(model) == snapshot

    def test_none(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=None)
        assert to_xml(model) == snapshot


class TestMediaType:
    class Model(XmlModel, tag="media-type"):
        value: MediaType = element()

    class OptionalModel(XmlModel, tag="media-type"):
        value: MediaType[str | None] = element()

    def test_true(self, snapshot: SnapshotAssertion):
        model = self.Model(value="application/xml")
        assert to_xml(model) == snapshot

    def test_type_only(self):
        with pytest.raises(ValidationError):
            self.Model(value="text")

    def test_invalid(self):
        with pytest.raises(ValidationError):
            self.Model(value="application/does-not-exist")

    def test_optional(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value="text/vtt")
        assert to_xml(model) == snapshot

    def test_invalid_optional(self):
        with pytest.raises(ValidationError):
            self.OptionalModel(value="application/does-not-exist")

    def test_none(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=None)
        assert to_xml(model) == snapshot


class TestCData:
    class Model(XmlModel, tag="cdata"):
        value: CData = element()

    class OptionalModel(XmlModel, tag="cdata"):
        value: CData[str | None] = element()

    def test_plain(self, snapshot: SnapshotAssertion):
        model = self.Model(value="This is some text.")
        assert to_xml(model) == snapshot

    def test_escaping(self, snapshot: SnapshotAssertion):
        model = self.Model(
            value="This <bold>text</bold> is long & contains characters that need escaping."
        )
        assert to_xml(model) == snapshot

    def test_optional(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value="This is some text.")
        assert to_xml(model) == snapshot

    def test_none(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=None)
        assert to_xml(model) == snapshot


class TestDurationInSeconds:
    class Model(XmlModel, tag="seconds"):
        value: DurationInSeconds = element()

    class OptionalModel(XmlModel, tag="seconds"):
        value: DurationInSeconds[timedelta | int | None] = element()

    def test_int(self, snapshot: SnapshotAssertion):
        model = self.Model(value=20)
        assert to_xml(model) == snapshot

    def test_timedelta(self, snapshot: SnapshotAssertion):
        model = self.Model(value=timedelta(minutes=1, seconds=10))
        assert to_xml(model) == snapshot

    def test_negative_timedelta(self):
        with pytest.raises(ValidationError):
            self.Model(value=timedelta(minutes=-1))

    def test_ignored_microseconds(self, snapshot: SnapshotAssertion):
        model = self.Model(value=timedelta(minutes=1, seconds=10, milliseconds=100, microseconds=200))
        assert to_xml(model) == snapshot

    def test_optional(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=200)
        assert to_xml(model) == snapshot

    def test_none(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=None)
        assert to_xml(model) == snapshot

class TestDateTime:
    class Model(XmlModel, tag="datetime"):
        value: DateTime = element()

    class OptionalModel(XmlModel, tag="datetime"):
        value: DateTime | None = element()

    def test_utc(self, snapshot: SnapshotAssertion):
        model = self.Model(value=datetime(2000, 12, 20, 14, 00, tzinfo=timezone.utc))
        assert to_xml(model) == snapshot

    def test_non_utc(self, snapshot: SnapshotAssertion):
        time_zone = ZoneInfo("Europe/Berlin")
        model = self.Model(value=datetime(2000, 12, 20, 14, 00, tzinfo=time_zone))
        assert to_xml(model) == snapshot

    def test_no_tz(self):
        with pytest.raises(ValidationError):
            self.Model(value=datetime(2000, 12, 20, 14, 00))

    def test_optional(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=datetime(2000, 12, 20, 14, 00, tzinfo=timezone.utc))
        assert to_xml(model) == snapshot

    def test_none(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=None)
        assert to_xml(model) == snapshot


class TestDuration:
    class Model(XmlModel, tag="duration"):
        value: Duration = element()

    class OptionalModel(XmlModel, tag="duration"):
        value: Duration[timedelta | int | None] = element()

    def test_int(self, snapshot: SnapshotAssertion):
        model = self.Model(value=20)
        assert to_xml(model) == snapshot

    def test_timedelta(self, snapshot: SnapshotAssertion):
        model = self.Model(value=timedelta(minutes=1, seconds=10, milliseconds=200))
        assert to_xml(model) == snapshot

    def test_negative_timedelta(self):
        with pytest.raises(ValidationError):
            self.Model(value=timedelta(minutes=-1))

    def test_ignored_microseconds(self, snapshot: SnapshotAssertion):
        model = self.Model(value=timedelta(minutes=1, seconds=10, milliseconds=100, microseconds=200))
        assert to_xml(model) == snapshot

    def test_optional(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=200)
        assert to_xml(model) == snapshot

    def test_none(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=None)
        assert to_xml(model) == snapshot


class TestLanguage:
    class Model(XmlModel, tag="language"):
        value: Language = element()

    class OptionalModel(XmlModel, tag="language"):
        value: Language[str | None] = element()

    def test_iso_639_1(self, snapshot: SnapshotAssertion):
        model = self.Model(value="en")
        assert to_xml(model) == snapshot

    def test_iso_639_3(self, snapshot: SnapshotAssertion):
        model = self.Model(value="eng")
        assert to_xml(model) == snapshot

    def test_bcp_47(self, snapshot: SnapshotAssertion):
        model = self.Model(value="en-us")
        assert to_xml(model) == snapshot

    def test_uppercase(self):
        with pytest.raises(ValidationError):
            self.Model(value="en-US")

    def test_optional(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value="en")
        assert to_xml(model) == snapshot

    def test_none(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=None)
        assert to_xml(model) == snapshot


class TestUUIDv5:
    class Model(XmlModel, tag="uuid5"):
        value: UUIDv5 = element()

    class OptionalModel(XmlModel, tag="uuid5"):
        value: UUIDv5[UUID | str | None] = element()

    def test_uuid(self, snapshot: SnapshotAssertion):
        model = self.Model(value=UUID('1F252349-FB78-541D-AEE2-613778F8EB08'))
        assert to_xml(model) == snapshot

    def test_catch_uuid_version(self):
        with pytest.raises(ValidationError):
            self.Model(value=uuid4())

    def test_string(self, snapshot: SnapshotAssertion):
        model = self.Model(value="1F252349-FB78-541D-AEE2-613778F8EB08")
        assert to_xml(model) == snapshot

    def test_uuid_string(self, snapshot: SnapshotAssertion):
        model = self.Model(value="urn:uuid:1F252349-FB78-541D-AEE2-613778F8EB08")
        assert to_xml(model) == snapshot

    def test_optional(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value="1F252349-FB78-541D-AEE2-613778F8EB08")
        assert to_xml(model) == snapshot

    def test_none(self, snapshot: SnapshotAssertion):
        model = self.OptionalModel(value=None)
        assert to_xml(model) == snapshot