from datetime import timedelta

from pydantic import Field, PositiveInt
from pydantic_xml import attr, computed_element, element, wrapped

from podryk.models.enum import EpisodeType
from podryk.models.field_types import (
    URL,
    CData,
    DateTime,
    DurationInSeconds,
    YesBool,
)
from podryk.models.namespaces import NAMESPACES, Namespace
from podryk.models.sub_types import (
    Chapter,
    Chapters,
    Enclosure,
    Guid,
    Transcript,
)
from podryk.models.xml_model import XmlModel


class Episode(XmlModel, tag="item", nsmap=NAMESPACES):
    title: str = element()
    """
    The title for the podcast episode.
    
    The title value is a string containing a concise name for your episode.
    Title values should not include season or episode numbers, as there are specific elements to capture those values.
    """

    enclosure: Enclosure = element()
    """
    The audio/video episode content, file size, and file type information.
    
    Supported file formats include MP3 (.mp3) and MPEG-4 (.m4a, .m4v, .mp4).
    """

    guid: Guid = element()
    """
    The globally unique identifier (GUID) for a podcast episode.
    
    Each episode must have a unique GUID that never changes. Values are case-sensitive strings.
    """

    # Optional fields
    link: URL | None = element(default=None)
    """
    The URL of a web page associated with the podcast episode.
    
    Useful when an episode has a corresponding webpage.
    """

    publication_date: DateTime | None = element(tag="pubDate", default=None)
    """The release date and time of an episode."""

    description: CData[str | None] = element(default=None)
    """
    The description of the podcast episode.
    """

    # Fields from itunes namespace

    duration: DurationInSeconds[timedelta | None] = element(ns=Namespace.ITUNES, default=None)
    """The duration of a podcast episode in seconds."""

    image: URL | None = wrapped(
        "image",
        ns=Namespace.ITUNES,
        entity=attr(name="href", default=None),
    )
    """
    The episode-specific artwork.
    
    Verify the web server hosting your image allows HTTP head requests.
    
    Image must be a minimum size of 1400 x 1400 pixels and a maximum size of 3000 x 3000 pixels,
    in JPEG or PNG format, 72 dpi, with appropriate file extensions (.jpg, .png), and in the sRGB colorspace.
    File type extension must match the actual file type of the image file.
    """
    explicit: bool | None = element(ns=Namespace.ITUNES, default=None)
    """
    The parental advisory information for a podcast episode.
    
    The value can be true, indicating the presence of explicit content, or false,
    indicating that a podcast doesn’t contain explicit language or adult content.
    """

    season_number: PositiveInt | None = element(tag="season", ns=Namespace.ITUNES, default=None)
    """The chronological number associated with a podcast episode's season."""

    episode_number: PositiveInt | None = element(tag="episode", ns=Namespace.ITUNES, default=None)
    """
    The chronological number that is associated with a podcast episode.
    
    This is required for serial podcasts.
    """

    type: EpisodeType | None = element(tag="episodeType", ns=Namespace.ITUNES, default=None)
    """Defines the type of content for a specific podcast episode."""

    block: YesBool[bool | None] = element(ns=Namespace.ITUNES, default=None)
    """Prevents a specific episode from appearing in podcast listening applications."""

    # Fields from podcast namespace

    transcripts: list[Transcript] | None = element(default=None)
    """A link to a transcript or closed captions file. Multiple tags can be present for multiple formats."""

    # Fields from podlove namespace

    chapters: list[Chapter] | None = Field(exclude=True, default=None)

    @computed_element
    def _chapters(self) -> Chapters | None:
        return Chapters(chapters=self.chapters) if self.chapters else None
