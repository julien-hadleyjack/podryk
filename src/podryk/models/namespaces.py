# noinspection HttpUrlsUsage
class Namespace(object):
    ITUNES = "itunes"
    PODCAST = "podcast"
    ATOM = "atom"
    CONTENT = "content"
    """Vocabulary for handling encoded content."""

    MEDIA = "media"
    DC_TERMS = "dcterms"
    """Dublin Core metadata terms to describe discovery/availability."""

    CHAPTERS = "psc"
    """Podlove's Simple Chapter for episode chapters."""


NAMESPACES = {
    Namespace.ITUNES: "http://www.itunes.com/dtds/podcast-1.0.dtd",
    Namespace.PODCAST: "https://podcastindex.org/namespace/1.0",
    Namespace.ATOM: "http://www.w3.org/2005/Atom",
    Namespace.CONTENT: "http://purl.org/rss/1.0/modules/content/",
    Namespace.MEDIA: "http://search.yahoo.com/mrss/",
    Namespace.DC_TERMS: "http://purl.org/dc/terms/",
    Namespace.CHAPTERS: "http://podlove.org/simple-chapters",
}
