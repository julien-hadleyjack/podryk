from datetime import datetime, timedelta, timezone

from syrupy import SnapshotAssertion

from podryk import Chapter, Enclosure, Episode, Guid, Transcript

from .utils.xml_util import to_xml


def test_minimal_episode(snapshot: SnapshotAssertion):
    episode = Episode(
        title="Episode title",
        guid=Guid(guid="https://example.com/episode.html"),
        enclosure=Enclosure(
            url="https://example.com/audio.mp3",
            length=30000,
            type="audio/mpeg",
        ),
    )

    assert to_xml(episode) == snapshot


def test_full_episode(snapshot: SnapshotAssertion):
    episode = Episode(
        title="Episode title",
        guid=Guid(guid="example-guid", is_permalink=True),
        enclosure=Enclosure(
            url="https://example.com/audio.mp3",
            length=30000,
            type="audio/mpeg",
        ),
        link="https://example.com",
        publication_date=datetime(2000, 7, 20, 10, 55, 40, tzinfo=timezone.utc),
        description="Episode description",
        duration=timedelta(hours=1, minutes=15, seconds=55, milliseconds=200),
        explicit=True,
        image="https://example.com/episode.png",
        block=True,
        transcripts=[
            Transcript(
                url="https://example.com/transcript.html",
                type="text/html",
                language="en",
            ),
            Transcript(
                url="https://example.com/transcript.vtt",
                type="text/vtt",
                language="de",
            ),
        ],
        chapters=[
            Chapter(
                start=timedelta(minutes=10, milliseconds=200),
                title="Chapter 1",
            )
        ],
    )

    assert to_xml(episode) == snapshot
