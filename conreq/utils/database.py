def add_unique(model, **kwargs) -> bool:
    """Save to the database only if the model is fully unique.
    Returns `True` if the operation was successful."""
    new_request = model(**kwargs)
    new_request.clean_fields()
    if model.objects.filter(**kwargs):
        return False
    new_request.save()
    return True
