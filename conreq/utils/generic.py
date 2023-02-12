"""Generic functions to be used anywhere. All functions only have stdlib dependencies."""
from re import sub


def remove_duplicates_from_list(duplicate_list: list) -> list:
    """Returns a list that contains no duplicate values."""
    return list(dict.fromkeys(duplicate_list))


def clean_string(
    string: str,
    allow_ascii: bool = True,
    rm_spaces: bool = True,
    rm_repeated_spaces: bool = True,
    rm_special_chars: bool = True,
    lowercase: bool = True,
    spaces: str = "-",
) -> str:
    """Removes non-alphanumerics from a string."""
    new_string = string
    if allow_ascii:
        new_string = string.encode("ascii", "ignore").decode()
    if rm_spaces:
        new_string = new_string.replace(" ", spaces)
    if rm_special_chars:
        new_string = sub(r"[^a-zA-Z0-9 ]+", "", new_string)
    if lowercase:
        new_string = new_string.lower()
    if rm_repeated_spaces:
        new_string = sub(r"  +", " ", new_string)
    return new_string


def list_intersection(list_1: list, list_2: list) -> list:
    """Returns a new list that is the intersection of two lists.
    Helps find duplicates between two lists."""
    return [value for value in list_1 if value in list_2]


class DoNothingDecorator:
    """Decorator that does nothing."""

    # pylint: disable=too-few-public-methods
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __call__(self, target, *args, **kwargs):
        return target


class DoNothingWith:
    """Class usable in a python `with` statement that does nothing."""

    def __enter__(self):
        pass

    def __exit__(self, *_):
        pass
