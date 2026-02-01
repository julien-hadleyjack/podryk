from syrupy import SnapshotAssertion

from podryk import Enclosure, Episode, Guid, Podcast, PodcastCategory

from .utils.xml_util import to_xml


def test_minimal_podcast(snapshot: SnapshotAssertion):
    podcast = Podcast(
        canonical_link="https://example.com/feed.rss",
        title="Podcast title",
        description="Podcast description",
        link="https://example.com/episode.html",
        language="en",
        image="https://example.com/podcast.png",
        explicit=False,
        episodes=[
            Episode(
                title="Episode title",
                guid=Guid(guid="example-guid"),
                enclosure=Enclosure(
                    url="https://example.com/audio.mp3",
                    length=30000,
                    type="audio/mpeg",
                ),
            )
        ],
    )

    assert to_xml(podcast) == snapshot


def test_full_podcast(snapshot: SnapshotAssertion):
    podcast = Podcast(
        canonical_link="https://example.com/feed.rss",
        title="Podcast title",
        description="Podcast description",
        link="https://example.com/episode.html",
        language="en",
        image="https://example.com/podcast.png",
        categories=[category for category in PodcastCategory],
        explicit=True,
        episodes=[
            Episode(
                title="Episode title",
                guid=Guid(guid="example-guid"),
                enclosure=Enclosure(
                    url="https://example.com/audio.mp3",
                    length=30000,
                    type="audio/mpeg",
                ),
            )
        ],
    )

    assert to_xml(podcast) == snapshot
