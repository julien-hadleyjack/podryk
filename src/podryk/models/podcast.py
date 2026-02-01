from typing import List
from uuid import UUID

from pydantic import Field
from pydantic_xml import BaseXmlModel, attr, computed_element, element, wrapped

from podryk.models.enum import PodcastCategory, PodcastType
from podryk.models.episode import Episode
from podryk.models.field_types import URL, CData, Language, UUIDv5, YesBool, YesNoBool
from podryk.models.namespaces import NAMESPACES, Namespace
from podryk.models.sub_types import AtomLink, Category, TextRecord
from podryk.models.xml_model import XmlModel


class Podcast(XmlModel, tag="channel", nsmap=NAMESPACES):
    canonical_link: URL = Field(exclude=True)
    """The declared canonical feed URL for the podcast."""

    title: str = element()
    """
    The podcast title. A string containing the name of a podcast and nothing else.
    
    Including keywords in an attempt to improve a podcast's search ranking,
    may result in being blocked from certain directories.
    """

    description: CData = element()
    """Text that describes a podcast to potential listeners."""

    link: URL = element()
    """The website or web page associated with a podcast."""

    language: Language = element()
    """The language that is spoken on the podcast, specified in the ISO 639 format."""

    episodes: List[Episode] = element(min_length=1)
    """Episodes in the podcast."""

    copyright: str | None = element(default=None)
    """
    The copyright details for a podcast.
    
    Should not include the word "Copyright", the © symbol, and/or a year.
    """

    # Fields from itunes namespace

    categories: List[PodcastCategory] = element(exclude=True, default_factory=list)
    """
    The category that best fits a podcast, selected from the list of Apple Podcasts categories:
    https://podcasters.apple.com/support/1691-apple-podcasts-categories
    """

    explicit: bool = element(ns=Namespace.ITUNES)
    """The parental advisory information for a podcast."""

    image: URL | None = wrapped(
        "image",
        ns=Namespace.ITUNES,
        entity=attr(name="href", default=None),
    )
    """
    The artwork for the podcast, specified by providing a URL linking to it.
    
    Verify the web server hosting your image allows HTTP head requests.

    Image must be a minimum size of 1400 x 1400 pixels and a maximum size of 3000 x 3000 pixels,
    in JPEG or PNG format, 72 dpi, with appropriate file extensions (.jpg, .png), and in the RGB colorspace.
    File type extension must match the actual file type of the image file.
    """

    author: str | None = element(ns=Namespace.ITUNES, default=None)
    """The group, person, or people responsible for creating the podcast."""

    type: PodcastType | None = element(ns=Namespace.ITUNES, default=None)
    """
    Specifies the podcast as either episodic or serial.
    
    Episodic is the default and assumed if this element is not present. This element is required for serial podcasts.
    """

    complete: YesBool[bool | None] = element(ns=Namespace.ITUNES, default=None)
    """Specifies that a podcast is complete and will not post any more episodes in the future."""

    # Fields from podcast namespace

    locked: YesNoBool[bool | None] = element(ns=Namespace.PODCAST, default=None)
    """Tells podcast hosting platforms whether they are allowed to import this feed."""

    guid: UUIDv5[UUID | str] | None = element(
        ns=Namespace.PODCAST, default=None
    )
    """
    The globally unique identifier (GUID) for a podcast.
    
    The value is a UUIDv5, and generated from the RSS feed URL,
    with the protocol scheme and trailing slashes stripped off,
    combined with a unique "podcast" namespace which has a UUID of ead4c236-bf58-58c6-a2c6-a6b28d128cb6.
    
    A podcast should be assigned a <podcast:guid> once in its lifetime,
    using its current feed URL at the time of assignment as the seed value.
    That GUID is then meant to follow the podcast from then on, for the duration of its existence,
    even if the feed URL changes. This means that when a podcast moves from one hosting platform to another,
    its <podcast:guid> should be discovered by the new host and imported into the new platform for inclusion
    into the feed.

    Using this pattern, podcasts can maintain a consistent identity across the open podcasting ecosystem without
    the need for a central authority.
    """

    text_records: list[TextRecord] | None = element(default=None)
    """
    A free-form text field to present a string in a podcast feed.
    
    One use case of this is to verify ownership. For example, a show owner may be asked 
    to add a unique text field to prove that they control the feed (and therefore the show).
    """

    @computed_element
    def _canonical_link(self) -> AtomLink:
        if isinstance(self.canonical_link, AtomLink):
            return self.canonical_link
        else:
            return AtomLink(href=self.canonical_link)

    @computed_element
    def _categories(self) -> list[Category] | None:
        results: dict[str, Category] = {}
        for category in self.categories:
            category_name, sub_category_name = category.category, category.sub_category

            # Add parent category
            if category_name not in results:
                results[category.category] = Category(text=category_name)

            parent = results[category.category]

            # Add sub category
            if sub_category_name and all(
                sub_category.text != sub_category
                for sub_category in parent.sub_categories
            ):
                parent.sub_categories.append(Category(text=sub_category_name))

        return list(results.values())

    def to_feed(self) -> bytes:
        return _PodcastFeed(channel=self).to_xml(
            xml_declaration=True,
            pretty_print=True,
            encoding="UTF-8",
            exclude_none=True,
            skip_empty=True,
        )


class _PodcastFeed(BaseXmlModel, tag="rss", nsmap=NAMESPACES):
    version: str = attr(default="2.0")
    channel: Podcast = element()
