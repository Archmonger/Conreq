from re import sub as substitution


def generate_cache_key(cache_name, cache_args, cache_kwargs, key):
    return clean_string(
        cache_name
        + "_args"
        + str(cache_args)
        + "_kwargs"
        + str(cache_kwargs)
        + "_key"
        + str(key)
    )


def obtain_key_from_cache_key(cache_key):
    # Returns values after the keyword "_key"
    return cache_key[cache_key.find("_key") + len("_key") :]


def is_key_value_in_list(search_list, key, value, return_item=False):
    # Iterate through each result and check for the key/value pair
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
        return string
