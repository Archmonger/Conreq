from datetime import datetime, timedelta


def tv_filters(filter_name=None):
    preset_filters = {
        "currently ongoing": {
            "sort_by": "popularity.desc",
            "air_date_gte": (datetime.today() - timedelta(days=7)).strftime(
                r"%Y-%m-%d"
            ),
            "air_date_lte": datetime.today().strftime(r"%Y-%m-%d"),
        },
        "airing today": {
            "sort_by": "popularity.desc",
            "air_date_gte": datetime.today().strftime(r"%Y-%m-%d"),
            "air_date_lte": datetime.today().strftime(r"%Y-%m-%d"),
        },
    }

    if filter_name:
        return preset_filters[filter_name]
    return preset_filters
