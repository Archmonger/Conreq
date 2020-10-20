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
