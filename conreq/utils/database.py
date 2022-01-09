def add_unique(model, **kwargs):
    """Adds a row to the database only if all parameters are unique."""
    new_request = model(**kwargs)
    new_request.clean_fields()
    if model.objects.filter(**kwargs):
        return
    new_request.save()
