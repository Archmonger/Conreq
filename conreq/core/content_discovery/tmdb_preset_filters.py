from datetime import datetime, timedelta


def tv_filters(filter_name=None):
    today = datetime.today()
    preset_filters = {
        "currently ongoing": {
            "sort_by": "popularity.desc",
            "air_date_gte": (today - timedelta(days=7)).strftime(r"%Y-%m-%d"),
            "air_date_lte": today.strftime(r"%Y-%m-%d"),
        },
        "airing today": {
            "sort_by": "popularity.desc",
            "air_date_gte": today.strftime(r"%Y-%m-%d"),
            "air_date_lte": today.strftime(r"%Y-%m-%d"),
        },
    }

    if filter_name:
        return preset_filters[filter_name]
    return preset_filters


def movie_filters(filter_name=None):
    today = datetime.today()
    preset_filters = {
        "coming soon": {
            "sort_by": "popularity.desc",
            "primary_release_date_gte": today.strftime(r"%Y-%m-%d"),
            "release_date_gte": today.strftime(r"%Y-%m-%d"),
            "primary_release_date_lte": (today + timedelta(days=365)).strftime(
                r"%Y-%m-%d"
            ),
            "release_date_lte": (today + timedelta(days=365)).strftime(r"%Y-%m-%d"),
        },
        "in theaters": {
            "sort_by": "popularity.desc",
            "with_release_type": "2|3",
            "primary_release_date_gte": (today - timedelta(days=150)).strftime(
                r"%Y-%m-%d"
            ),
            "release_date_gte": (today - timedelta(days=150)).strftime(r"%Y-%m-%d"),
        },
    }

    if filter_name:
        return preset_filters[filter_name]
    return preset_filters