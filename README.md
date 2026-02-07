# podryk: A podcast feed generator

An RSS 2.0 feed writer for Python for generating Podcast feeds. Supported features:

- [RSS 2.0](http://www.rssboard.org/rss-2-0)
- [iTunes](https://help.apple.com/itc/podcasts_connect/#/itcb54353390) (Apple Podcast Connect)
- [Podlove](https://podlove.org/simple-chapters/): chapters
- [Podcasting 2.0](https://podcasting2.org/docs/podcast-namespace): transcripts & text records

Podryk is opinionated: If there is multiple conflicting specifications for a feature (like chapters), only one will be implemented.

## Installation

You can install the python library with:

```bash
pip install podryk
```

## Usage

An example with only required attributes:

<!-- [[[cog
from scripts.cog_readme import print_example
from test_readme import test_minimal_feed
print_example(test_minimal_feed)
]]] -->
```python
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
```
<!-- [[[end]]] -->

An example with all possible attributes:

<!-- [[[cog
from test_readme import test_full_feed
print_example(test_full_feed)
]]] -->
```python
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
```
<!-- [[[end]]] -->



## Miscellaneous

Podryk implements a subset from the following Podcast specifications:

- [PSP-1: The Podcast RSS Standard](https://github.com/Podcast-Standards-Project/PSP-1-Podcast-RSS-Specification)
- [Podcasting 2.0](https://podcasting2.org/docs/podcast-namespace)
- [Spotify's Podcast Delivery Specification](https://support.spotify.com/us/creators/article/podcast-specification-doc/)
- [iTunes' Podcast RSS feed requirements](https://podcasters.apple.com/support/823-podcast-requirements)

Create a ticket if you find any deviations from the mentioned specifications. 

You can validate your podcast feed using one of these services:

- https://www.castfeedvalidator.com/
- https://podba.se/validate/
- https://podcasters.apple.com/support/829-validate-your-podcast

