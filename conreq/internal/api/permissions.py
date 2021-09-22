import typing

from django.http import HttpRequest
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import BaseHasAPIKey, KeyParser


class HasAPIKey(BaseHasAPIKey):
    model = APIKey
    key_parser = KeyParser()

    def get_key(self, request: HttpRequest) -> typing.Optional[str]:
        # Prefer key in header
        header_key = self.key_parser.get(request)
        if header_key:
            return header_key
        # Fallback to key in URL parameters
        return request.GET.get("apikey")
