import textwrap
from datetime import datetime, timedelta, timezone

from syrupy import SnapshotAssertion

from podryk import (
    Enclosure,
    Episode,
    EpisodeType,
    Guid,
    Podcast,
    PodcastCategory,
    PodcastType,
)


def test_spotify_example_feed(snapshot: SnapshotAssertion):
    """Similar to the simple example from Spotify's "Podcast Delivery Specification"."""
    feed = Podcast(
        canonical_link="https://example.com/canonical.rss",
        title="Serial",
        description=textwrap.dedent(
            """
            Serial is a new podcast from the creators of This American Life,
            hosted by Sarah Koenig. Serial unfolds one story - a true story - over the course of a whole
            season. The show follows the plot and characters wherever they lead, through many surprising
            twists and turns. Sarah won't know what happens at the end of the story until she gets there, not
            long before you get there with her. Each week she'll bring you the latest chapter, so it's
            important to listen in, starting with Episode 1. New episodes are released on Thursday
            mornings. Serial, like This American Life, is a production of WBEZ Chicago.
            """
        )
        .replace("\n", " ")
        .strip(),
        link="https://serialpodcast.org",
        language="en",
        author="This America Life",
        categories=[PodcastCategory.POLITICS],
        type=PodcastType.EPISODIC,
        image="https://serialpodcast.org/sites/all/modules/custom/serial/img/serial-itunes-logo.png",
        explicit=False,
        episodes=[
            Episode(
                title="Episode 09: To Be Suspected",
                guid=Guid(guid="1234"),
                description=textwrap.dedent(
                    """
                    New information is coming in about what maybe did not happen on
                    January 13, 1999. And while the memory of that day is foggy at best, he does remember what
                    happened next: being questioned, being arrested and, a little more than a year later, being
                    sentenced to life in prison.
                    """
                )
                .replace("\n", " ")
                .strip(),
                publication_date=datetime(2014, 11, 20, 10, 30, tzinfo=timezone.utc),
                duration=timedelta(seconds=2700),
                enclosure=Enclosure(
                    url="https://dts.podtrac.com/redirect.mp3/files.serialpodcast.org/sites/default/files/podcast/14224",
                    length=30000,
                    type="audio/mpeg",
                ),
            )
        ],
    ).to_feed()

    assert feed.decode() == snapshot


def test_itunes_example_feed(snapshot: SnapshotAssertion):
    """Similar to the RSS feed sample from Apple's "A Podcaster's Guide to RSS"."""
    feed = Podcast(
        canonical_link="https://example.com",
        title="Hiking Treks",
        link="https://www.apple.com/itunes/podcasts/",
        language="en-us",
        copyright="© 2020 John Appleseed",
        author="The Sunset Explorers",
        description="""
        Love to get outdoors and discover nature&apos;s treasures? Hiking Treks is the
        show for you. We review hikes and excursions, review outdoor gear and interview
        a variety of naturalists and adventurers. Look for new episodes each week.
        """,
        type=PodcastType.SERIAL,
        image="https://applehosted.podcasts.apple.com/hiking_treks/artwork.png",
        categories=[PodcastCategory.WILDERNESS],
        explicit=False,
        episodes=[
            Episode(
                type=EpisodeType.TRAILER,
                title="Hiking Treks Trailer",
                description="""
                The Sunset Explorers share tips, techniques and recommendations for
                great hikes and adventures around the United States. Listen on 
                <a href="https://www.apple.com/itunes/podcasts/">Apple Podcasts</a>.
                """,
                enclosure=Enclosure(
                    length=498537,
                    type="audio/mpeg",
                    url="http://example.com/podcasts/everything/AllAboutEverythingEpisode4.mp3",
                ),
                guid=Guid(guid="D03EEC9B-B1B4-475B-92C8-54F853FA2A22"),
                publication_date=datetime(2019, 1, 8, 1, 15, tzinfo=timezone.utc),
                duration=timedelta(seconds=1079),
                explicit=False,
            ),
            Episode(
                type=EpisodeType.FULL,
                episode_number=4,
                season_number=2,
                title="S02 EP04 Mt. Hood, Oregon",
                description="Tips for trekking around the tallest mountain in Oregon",
                enclosure=Enclosure(
                    length=8727310,
                    type="audio/mp4",
                    url="http://example.com/podcasts/everything/mthood.m4a",
                ),
                guid=Guid(guid="22BCFEBF-44FB-4A19-8229-7AC678629F57"),
                publication_date=datetime(2019, 5, 7, 12, 0, tzinfo=timezone.utc),
                duration=timedelta(seconds=1024),
                explicit=False,
            ),
        ],
    ).to_feed()

    assert feed.decode() == snapshot
