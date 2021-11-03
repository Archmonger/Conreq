import typing

from django.http import HttpRequest
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import BaseHasAPIKey, KeyParser


class HasAPIKey(BaseHasAPIKey):
    model = APIKey
    key_parser = KeyParser()

    def get_key(self, request: HttpRequest) -> typing.Optional[str]:
        # Prefer key in header, fallback to URL parameters.
        return self.key_parser.get(request) or request.GET.get("apikey")
