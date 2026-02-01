from __future__ import annotations

import uuid

from pydantic import (
    HttpUrl,
    TypeAdapter,
    ValidationError,
    model_validator,
)
from pydantic_xml import attr, element

from podryk.models.enum import AtomLinkRel
from podryk.models.field_types import URL, Duration, MediaType
from podryk.models.namespaces import NAMESPACES, Namespace
from podryk.models.xml_model import XmlModel


class Guid(XmlModel, tag="guid"):
    """Globally unique identifier for an episode."""

    is_permalink: bool | None = attr(name="isPermaLink")
    guid: str | URL | uuid.UUID

    @model_validator(mode="before")
    @classmethod
    def set_permalink_default(cls, data: dict) -> dict:
        guid = data.get("guid")
        is_permalink = data.get("is_permalink")

        if is_permalink is None:
            try:
                TypeAdapter(HttpUrl).validate_python(guid)
                data["is_permalink"] = None
            except ValidationError:
                data["is_permalink"] = False

        return data


class Enclosure(XmlModel, tag="enclosure"):
    """The audio/video episode content, file size, and file type information."""

    url: URL = attr()
    """Location of the media file."""

    length: int = attr()
    """The length of the file in bytes."""

    type: MediaType = attr()
    """MIME type of the media file."""


class Transcript(XmlModel, tag="transcript", ns=Namespace.PODCAST):
    url: URL = attr()
    type: MediaType = attr()
    language: str | None = attr(default=None)


class Chapter(XmlModel, tag="chapter", ns=Namespace.CHAPTERS):
    start: Duration = attr()
    """Refers to a point in time relative to the start of the media file."""
    title: str = attr()
    """Title of the chapter."""
    href: URL | None = attr(default=None)
    """External link that provides related information to the chapter."""

    image: URL | None = attr(default=None)
    """External link to an image associated with the chapter. The image should have a 1:1 aspect ratio."""


class Chapters(XmlModel, tag="chapters", ns=Namespace.CHAPTERS):
    version: str = attr(default="1.2")
    chapters: list[Chapter] = element()


class AtomLink(XmlModel, tag="link", ns=Namespace.ATOM):
    href: URL = attr()
    rel: AtomLinkRel = attr(default=AtomLinkRel.SELF)
    type: MediaType = attr(default="application/rss+xml")


class TextRecord(XmlModel, tag="txt", ns=Namespace.PODCAST):
    """
    A free-form text field to present a string in a podcast feed.

    One use case of this is to verify ownership. For example, a show owner may be asked
    to add a unique text field to prove that they control the feed (and therefore the show).
    """

    purpose: str | None = attr(default=None)
    """A service specific string to denote the purpose for the field."""

    content: str


class Category(XmlModel, tag="category", ns=Namespace.ITUNES, nsmap=NAMESPACES):
    text: str = attr()
    sub_categories: list[Category] = element(default_factory=list)
