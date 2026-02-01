from enum import Enum, StrEnum, auto, unique


@unique
class Explicit(StrEnum):
    YES = auto()
    NO = auto()
    CLEAN = auto()


@unique
class PodcastType(StrEnum):
    EPISODIC = auto()
    SERIAL = auto()


@unique
class EpisodeType(StrEnum):
    FULL = auto()
    """A complete podcast episode"""

    TRAILER = auto()
    """A short promotional or preview episode for a podcast"""

    BONUS = auto()
    """
    Additional content that is unlike a typical episode
    (e.g., behind-the-scenes or a promotional episode for another podcast)
    """


@unique
class AtomLinkRel(StrEnum):
    ALTERNATE = auto()
    RELATED = auto()
    SELF = auto()
    ENCLOSURE = auto()
    VIA = auto()


@unique
class PodcastCategory(Enum):
    ARTS = ("Arts", None)
    BOOKS = ("Arts", "Books")
    DESIGN = ("Arts", "Design")
    FASHION_AND_BEAUTY = ("Arts", "Fashion & Beauty")
    FOOD = ("Arts", "Food")
    PERFORMING_ARTS = ("Arts", "Performing Arts")
    VISUAL_ARTS = ("Arts", "Visual Arts")

    BUSINESS = ("Business", None)
    CAREERS = ("Business", "Careers")
    ENTREPRENEURSHIP = ("Business", "Entrepreneurship")
    INVESTING = ("Business", "Investing")
    MANAGEMENT = ("Business", "Management")
    MARKETING = ("Business", "Marketing")
    NON_PROFIT = ("Business", "Non-Profit")

    COMEDY = ("Comedy", None)
    COMEDY_INTERVIEWS = ("Comedy", "Comedy Interviews")
    IMPROV = ("Comedy", "Improv")
    STAND_UP = ("Comedy", "Stand-Up")

    EDUCATION = ("Education", None)
    COURSES = ("Education", "Courses")
    HOW_TO = ("Education", "How To")
    LANGUAGE_LEARNING = ("Education", "Language Learning")
    SELF_IMPROVEMENT = ("Education", "Self-Improvement")

    FICTION = ("Fiction", None)
    COMEDY_FICTION = ("Fiction", "Comedy Fiction")
    DRAMA = ("Fiction", "Drama")
    SCIENCE_FICTION = ("Fiction", "Science Fiction")

    GOVERNMENT = ("Government", None)

    HISTORY = ("History", None)

    HEALTH_AND_FITNESS = ("Health & Fitness", None)
    ALTERNATIVE_HEALTH = ("Health & Fitness", "Alternative Health")
    FITNESS = ("Health & Fitness", "Fitness")
    MEDICINE = ("Health & Fitness", "Medicine")
    MENTAL_HEALTH = ("Health & Fitness", "Mental Health")
    NUTRITION = ("Health & Fitness", "Nutrition")
    SEXUALITY = ("Health & Fitness", "Sexuality")

    KIDS_AND_FAMILY = ("Kids & Family", None)
    EDUCATION_FOR_KIDS = ("Kids & Family", "Education for Kids")
    PARENTING = ("Kids & Family", "Parenting")
    PETS_AND_ANIMALS = ("Kids & Family", "Pets & Animals")
    STORIES_FOR_KIDS = ("Kids & Family", "Stories for Kids")

    LEISURE = ("Leisure", None)
    ANIMATION_AND_MANGA = ("Leisure", "Animation & Manga")
    AUTOMOTIVE = ("Leisure", "Automotive")
    AVIATION = ("Leisure", "Aviation")
    CRAFTS = ("Leisure", "Crafts")
    GAMES = ("Leisure", "Games")
    HOBBIES = ("Leisure", "Hobbies")
    HOME_AND_GARDEN = ("Leisure", "Home & Garden")
    VIDEO_GAMES = ("Leisure", "Video Games")

    MUSIC = ("Music", None)
    MUSIC_COMMENTARY = ("Music", "Music Commentary")
    MUSIC_HISTORY = ("Music", "Music History")
    MUSIC_INTERVIEWS = ("Music", "Music Interviews")

    NEWS = ("News", None)
    BUSINESS_NEWS = ("News", "Business News")
    DAILY_NEWS = ("News", "Daily News")
    ENTERTAINMENT_NEWS = ("News", "Entertainment News")
    NEWS_COMMENTARY = ("News", "News Commentary")
    POLITICS = ("News", "Politics")
    SPORTS_NEWS = ("News", "Sports News")
    TECH_NEWS = ("News", "Tech News")

    RELIGION_AND_SPIRITUALITY = ("Religion & Spirituality", None)
    BUDDHISM = ("Religion & Spirituality", "Buddhism")
    CHRISTIANITY = ("Religion & Spirituality", "Christianity")
    HINDUISM = ("Religion & Spirituality", "Hinduism")
    ISLAM = ("Religion & Spirituality", "Islam")
    JUDAISM = ("Religion & Spirituality", "Judaism")
    RELIGION = ("Religion & Spirituality", "Religion")
    SPIRITUALITY = ("Religion & Spirituality", "Spirituality")

    SCIENCE = ("Science", None)
    ASTRONOMY = ("Science", "Astronomy")
    CHEMISTRY = ("Science", "Chemistry")
    EARTH_SCIENCES = ("Science", "Earth Sciences")
    LIFE_SCIENCES = ("Science", "Life Sciences")
    MATHEMATICS = ("Science", "Mathematics")
    NATURAL_SCIENCES = ("Science", "Natural Sciences")
    NATURE = ("Science", "Nature")
    PHYSICS = ("Science", "Physics")
    SOCIAL_SCIENCES = ("Science", "Social Sciences")

    SOCIETY_AND_CULTURE = ("Society & Culture", None)
    DOCUMENTARY = ("Society & Culture", "Documentary")
    PERSONAL_JOURNALS = ("Society & Culture", "Personal Journals")
    PHILOSOPHY = ("Society & Culture", "Philosophy")
    PLACES_AND_TRAVEL = ("Society & Culture", "Places & Travel")
    RELATIONSHIPS = ("Society & Culture", "Relationships")

    SPORTS = ("Sports", None)
    BASEBALL = ("Sports", "Baseball")
    BASKETBALL = ("Sports", "Basketball")
    CRICKET = ("Sports", "Cricket")
    FANTASY_SPORTS = ("Sports", "Fantasy Sports")
    FOOTBALL = ("Sports", "Football")
    GOLF = ("Sports", "Golf")
    HOCKEY = ("Sports", "Hockey")
    RUGBY = ("Sports", "Rugby")
    RUNNING = ("Sports", "Running")
    SOCCER = ("Sports", "Soccer")
    SWIMMING = ("Sports", "Swimming")
    TENNIS = ("Sports", "Tennis")
    VOLLEYBALL = ("Sports", "Volleyball")
    WILDERNESS = ("Sports", "Wilderness")
    WRESTLING = ("Sports", "Wrestling")

    TECHNOLOGY = ("Technology", None)

    TRUE_CRIME = ("True Crime", None)

    TV_AND_FILM = ("TV & Film", None)
    AFTER_SHOWS = ("TV & Film", "After Shows")
    FILM_HISTORY = ("TV & Film", "Film History")
    FILM_INTERVIEWS = ("TV & Film", "Film Interviews")
    FILM_REVIEWS = ("TV & Film", "Film Reviews")
    TV_REVIEWS = ("TV & Film", "TV Reviews")

    def __init__(self, category: str | None, sub_category: str):
        self.category = category
        self.sub_category = sub_category
