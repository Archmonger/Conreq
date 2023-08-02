from datetime import datetime, timedelta

from django.utils.text import slugify

no_anime_values = {
    "overwrite:with_original_language": "en",
    "without_keywords": "210024",
}
anime_only_values = {
    "overwrite:with_original_language": "ja",
    "with_keywords": "210024",
}


def add_filter_values(new_values, current_filter):
    """Combines values from one filter dict into another."""
    for key, value in new_values.items():
        if key.startswith("overwrite:"):
            current_filter[key.replace("overwrite:", "")] = value

        elif current_filter.__contains__(key):
            current_filter[key] = f"{current_filter[key]},{value}"

        else:
            current_filter[key] = value


def preprocess_filters(preset_filters, slug, add_values):
    """Do any preprocessing needed on the filters"""
    processed_filters = {}

    for key in preset_filters:
        # Add any filter values needed
        if add_values:
            add_filter_values(add_values, preset_filters[key])

        # Slugify all filter names
        if slug:
            processed_filters[slugify(key)] = preset_filters[key]

    return processed_filters if processed_filters else preset_filters


def combined_filters(filter_name=None, slug=False, add_values=()):
    """These filters are automatically merged into TV and Movies."""
    today = datetime.now()
    preset_filters = {
        "new and loved": {
            "sort_by": "vote_average.desc",
            "vote_count.gte": "25",
            "first_air_date.gte": (today - timedelta(days=365)).strftime(r"%Y-%m-%d"),
            "first_air_date.lte": today.strftime(r"%Y-%m-%d"),
            "primary_release_date.gte": (today - timedelta(days=365)).strftime(
                r"%Y-%m-%d"
            ),
            "primary_release_date.lte": today.strftime(r"%Y-%m-%d"),
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "all time favorite": {
            "sort_by": "vote_average.desc",
            "vote_count.gte": "300",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "coming soon": {
            "sort_by": "popularity.desc",
            "first_air_date.gte": today.strftime(r"%Y-%m-%d"),
            "first_air_date.lte": (today + timedelta(days=365)).strftime(r"%Y-%m-%d"),
            "primary_release_date.gte": today.strftime(r"%Y-%m-%d"),
            "primary_release_date.lte": (today + timedelta(days=365)).strftime(
                r"%Y-%m-%d"
            ),
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "top rated": {
            "sort_by": "vote_average.desc",
            "vote_count.gte": "50",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "popular": {
            "sort_by": "popularity.desc",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "family friendly": {
            "sort_by": "popularity.desc",
            "with_genres": "10751|10762",
            "without_genres": "27,53,99,18",
            "with_original_language": "en|ja",
        },
        "action and adventure": {
            "sort_by": "popularity.desc",
            "with_genres": "10759|28|12",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "science fiction and fantasy": {
            "sort_by": "popularity.desc",
            "with_genres": "10765|878|14",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "drama": {
            "sort_by": "popularity.desc",
            "with_genres": "18",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "mystery": {
            "sort_by": "popularity.desc",
            "with_genres": "9648",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "crime": {
            "sort_by": "popularity.desc",
            "with_genres": "80",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "comedy": {
            "sort_by": "popularity.desc",
            "with_genres": "35",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "western": {
            "sort_by": "popularity.desc",
            "with_genres": "37",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
        "documentary": {
            "sort_by": "popularity.desc",
            "with_genres": "99",
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
    }

    preset_filters = preprocess_filters(preset_filters, slug, add_values)

    return preset_filters[filter_name] if filter_name else preset_filters


def tv_filters(filter_name=None, slug=False, add_values=()):
    """Predefined categories shown for the TV filter modal."""
    today = datetime.now()
    preset_filters = {
        "currently ongoing": {
            "sort_by": "popularity.desc",
            "air_date.gte": (today - timedelta(days=7)).strftime(r"%Y-%m-%d"),
            "air_date.lte": today.strftime(r"%Y-%m-%d"),
            "without_genres": "10751|10762|10763",  # No kids shows or news
            "with_original_language": "en|ja",
        },
        "airing today": {
            "sort_by": "popularity.desc",
            "air_date.gte": today.strftime(r"%Y-%m-%d"),
            "air_date.lte": today.strftime(r"%Y-%m-%d"),
            "without_genres": "10751|10762|10763",  # No kids shows or news
            "with_original_language": "en|ja",
        },
    }

    preset_filters = preprocess_filters(preset_filters, slug, add_values)

    preset_filters = {
        **preset_filters,
        **combined_filters(slug=slug, add_values=add_values),
    }

    return preset_filters[filter_name] if filter_name else preset_filters


def movie_filters(filter_name=None, slug=False, add_values=()):
    """Predefined categories shown in the movie filter modal."""
    today = datetime.now()
    preset_filters = {
        "in theaters": {
            "sort_by": "popularity.desc",
            "with_release_type": "2|3",
            "primary_release_date.gte": (today - timedelta(days=150)).strftime(
                r"%Y-%m-%d"
            ),
            "without_genres": "10751|10762",  # No kids shows
            "with_original_language": "en|ja",
        },
    }

    preset_filters = preprocess_filters(preset_filters, slug, add_values)

    preset_filters = {
        **preset_filters,
        **combined_filters(slug=slug, add_values=add_values),
    }

    return preset_filters[filter_name] if filter_name else preset_filters
