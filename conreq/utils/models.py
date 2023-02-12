import os
import uuid

from django.utils.deconstruct import deconstructible


@deconstructible
class UUIDFilePath:
    """Use this within an `upload_to = ...` parameter within a `FieldField` or
    `ImageField` in order to automatically change the filename to a UUID."""

    def __init__(self, path: str = ""):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename: str):
        extension = os.path.splitext(filename)[1]
        return str(self.path % (uuid.uuid4(), extension)).lstrip("/")
