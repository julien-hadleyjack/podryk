from syrupy import SnapshotAssertion


def test_minimal_feed(snapshot: SnapshotAssertion):
    from podryk import Enclosure, Episode, Guid, Podcast

    feed = Podcast(
        canonical_link="https://example.com/canonical.rss",
        title="Podcast title",
        description="Podcast description",
        link="https://example.com/episode.html",
        language="en",
        explicit=False,
        image="https://example.com/podcast.png",
        episodes=[
            Episode(
                title="Episode title",
                guid=Guid(guid="12345678-1234-5678-1234-567812345678"),
                enclosure=Enclosure(
                    url="https://example.com/audio.mp3",
                    length=30000,
                    type="audio/mpeg",
                ),
            )
        ],
    ).to_feed()

    assert feed.decode() == snapshot


def test_full_feed(snapshot: SnapshotAssertion):
    from datetime import datetime, timedelta, timezone

    from podryk import (
        Chapter,
        Enclosure,
        Episode,
        EpisodeType,
        Guid,
        Podcast,
        PodcastCategory,
        PodcastType,
        TextRecord,
        Transcript,
    )

    feed = Podcast(
        canonical_link="https://example.com/canonical.rss",
        title="Podcast title",
        description="Podcast description",
        link="https://example.com/episode.html",
        language="en",
        copyright="Copyright notice",
        categories=[
            PodcastCategory.FILM_REVIEWS,
            PodcastCategory.FILM_INTERVIEWS,
        ],
        explicit=True,
        image="https://example.com/podcast.png",
        author="Podcast author",
        type=PodcastType.SERIAL,
        complete=False,
        locked=False,
        guid="3595bd1c-50a4-504d-baf4-99de513b3737",
        text_records=[TextRecord(purpose="verify", content="S6lpp-7ZCn8-dZfGc-OoyaG")],
        episodes=[
            Episode(
                title="Episode title",
                guid=Guid(guid="12345678-1234-5678-1234-567812345678"),
                enclosure=Enclosure(
                    url="https://example.com/audio.mp3",
                    length=30000,
                    type="audio/mpeg",
                ),
                link="https://example.com/episode.html",
                publication_date=datetime(2014, 6, 20, 10, 35, tzinfo=timezone.utc),
                description="Episode description",
                duration=timedelta(hours=1, minutes=10, seconds=50),
                image="https://example.com/episode.png",
                explicit=False,
                season_number=2,
                episode_number=30,
                type=EpisodeType.FULL,
                block=False,
                transcripts=[
                    Transcript(url="https://example.com/episode.vtt", type="text/vtt"),
                ],
                chapters=[
                    Chapter(start=timedelta(seconds=10), title="Episode chapter 1"),
                    Chapter(
                        start=timedelta(minutes=2),
                        title="Episode chapter 2",
                        href="https://example.com/chapter.html",
                    ),
                ],
            )
        ],
    ).to_feed()

    assert feed.decode() == snapshot
