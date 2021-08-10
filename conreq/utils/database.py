def add_unique_to_db(model, **kwargs):
    """Adds a row to the database only if all parameters are unique."""
    if not model.objects.filter(**kwargs):
        new_request = model(**kwargs)
        new_request.clean_fields()
        new_request.save()
        return new_request
