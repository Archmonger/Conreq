from re import sub as substitution

from conreq.core import log

# Create a logger (for log files)
__logger = log.get_logger("Generic Tools")
log.configure(__logger, log.DEBUG)


def is_key_value_in_list(search_list, key, value, return_item=False):
    # Iterate through each result and check for the key/value pair
    # TODO: Add threading
    for item in search_list:
        if item.__contains__(key) and item[key] == value:
            if return_item:
                return item
            return True

    # The key value pair could not be found in the list of dictionaries
    return False


def clean_string(string):
    # Removes non-alphanumerics from a string
    try:
        return substitution(r"\W+", "", string).lower()
    except:
        log.handler(
            "Cleaning the string failed!",
            log.ERROR,
            __logger,
        )
        return string
