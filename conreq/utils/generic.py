"""Generic functions to be used anywhere. All functions only have stdlib dependencies."""
from re import sub


def is_key_value_in_list(
    key: any, value: any, search_list: list, return_item: bool = False
) -> bool:
    """Iterate through a list of dicts to check if a specific key/value pair exists."""
    if isinstance(search_list, list):
        for item in search_list:
            if item.__contains__(key) and item[key] == value:
                if return_item:
                    return item
                return True
    return False


def replace_item_in_list(search_for, replace_with, search_list):
    "Replaces matching items in a list with a replacement value"
    return [replace_with if x == search_for else x for x in search_list]


def remove_duplicates_from_list(duplicate_list: list) -> list:
    """Returns a list that contains no duplicate values"""
    return list(dict.fromkeys(duplicate_list))


def clean_string(
    string: str,
    spaces: bool = True,
    special_chars: bool = True,
    lowercase: bool = True,
    spaces_replacement: str = "",
) -> str:
    """Removes non-alphanumerics from a string"""
    new_string = string.encode("ascii", "ignore").decode()
    if not spaces:
        new_string = new_string.replace(" ", spaces_replacement)
    if not special_chars:
        new_string = sub(r"[^a-zA-Z0-9 ]+", "", new_string)
    if lowercase:
        new_string = new_string.lower()
    new_string = sub(r"  +", " ", new_string)
    return new_string


def str_to_bool(string: str, default_value: bool = True) -> bool:
    """Converts a string into a boolean."""
    if isinstance(string, str):
        if string.lower() == "true" or string == "1":
            return True
        if string.lower() == "false" or string == "0":
            return False
    return default_value


def str_to_int(value: str, default_value: int = 0) -> int:
    """Converts a string into a integer."""
    if isinstance(value, str) and value.isdigit():
        return int(value)
    if isinstance(value, int):
        return value
    return default_value
