from datetime import datetime, timedelta


def combined_filters(filter_name=None):
    """These filters are automatically merged into TV and Movies."""
    today = datetime.today()
    preset_filters = {
        "top rated": {
            "sort_by": "vote_average.desc",
            "vote_count.gte": 300,
            "without_keywords": "10103,161155",
        },
        "most popular": {
            "sort_by": "popularity.desc",
            "without_keywords": "10103,161155",
        },
        "english top rated": {
            "sort_by": "vote_average.desc",
            "vote_count.gte": 300,
            "with_original_language": "en",
            "without_keywords": "10103,161155",
        },
        "english most popular": {
            "sort_by": "popularity.desc",
            "with_original_language": "en",
            "without_keywords": "10103,161155",
        },
        "new and loved": {
            "sort_by": "vote_average.desc",
            "vote_count.gte": 50,
            "first_air_date.gte": (today - timedelta(days=365)).strftime(r"%Y-%m-%d"),
            "first_air_date.lte": today.strftime(r"%Y-%m-%d"),
            "primary_release_date.gte": (today - timedelta(days=365)).strftime(
                r"%Y-%m-%d"
            ),
            "primary_release_date.lte": today.strftime(r"%Y-%m-%d"),
            "without_keywords": "10103,161155",
        },
        "all time favorites": {
            "sort_by": "vote_average.desc",
            "vote_count.gte": 1500,
            "without_keywords": "10103,161155",
        },
        "child friendly": {
            "sort_by": "popularity.desc",
            "with_keywords": 10103,
        },
        "anime": {
            "sort_by": "popularity.desc",
            "with_genres": 16,
            "with_keywords": 210024,
            "without_keywords": "10103,161155",
        },
        "action and adventure": {
            "sort_by": "popularity.desc",
            "vote_count.gte": 50,
            "with_genres": 10759,
            "without_keywords": "10103,161155",
        },
        "drama": {
            "sort_by": "popularity.desc",
            "vote_count.gte": 50,
            "with_genres": 18,
            "without_keywords": "10103,161155",
        },
        "mystery": {
            "sort_by": "popularity.desc",
            "vote_count.gte": 50,
            "with_genres": 9648,
            "without_keywords": "10103,161155",
        },
        "comedy": {
            "sort_by": "popularity.desc",
            "vote_count.gte": 50,
            "with_genres": 35,
            "without_keywords": "10103,161155",
        },
        "documentary": {
            "sort_by": "popularity.desc",
            "vote_count.gte": 50,
            "with_genres": 99,
            "without_keywords": "10103,161155",
        },
    }

    if filter_name:
        return preset_filters[filter_name]
    return preset_filters


def tv_filters(filter_name=None):
    """Predefined categories shown for the TV filter modal."""
    today = datetime.today()
    preset_filters = {
        "currently ongoing": {
            "sort_by": "popularity.desc",
            "air_date.gte": (today - timedelta(days=7)).strftime(r"%Y-%m-%d"),
            "air_date.lte": today.strftime(r"%Y-%m-%d"),
            "without_genres": 10763,
            "without_keywords": "10103,161155",
        },
        "airing today": {
            "sort_by": "popularity.desc",
            "air_date.gte": today.strftime(r"%Y-%m-%d"),
            "air_date.lte": today.strftime(r"%Y-%m-%d"),
            "without_genres": 10763,
            "without_keywords": "10103,161155",
        },
        **combined_filters(),
    }

    if filter_name:
        return preset_filters[filter_name]
    return preset_filters


def movie_filters(filter_name=None):
    """Predefined categories shown in the movie filter modal."""
    today = datetime.today()
    preset_filters = {
        "coming soon": {
            "sort_by": "popularity.desc",
            "primary_release_date.gte": today.strftime(r"%Y-%m-%d"),
            "primary_release_date.lte": (today + timedelta(days=365)).strftime(
                r"%Y-%m-%d"
            ),
            "without_keywords": "10103,161155",
        },
        "in theaters": {
            "sort_by": "popularity.desc",
            "with_release_type": "2|3",
            "primary_release_date.gte": (today - timedelta(days=150)).strftime(
                r"%Y-%m-%d"
            ),
            "without_keywords": "10103,161155",
        },
        **combined_filters(),
    }

    if filter_name:
        return preset_filters[filter_name]
    return preset_filters