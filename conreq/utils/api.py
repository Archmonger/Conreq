from dataclasses import dataclass, field
from typing import Union

from drf_yasg import inspectors, openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


@dataclass
class APIDocs:
    """Information that can be passed into an `swagger_auto_schema`.
    See drf-yasg docs for more information."""

    # TODO: Add docstrings to all of these fields.
    method: str = None
    methods: list[str] = None
    # auto_schema = unset
    request_body: Union[
        openapi.Schema, openapi.SchemaRef, serializers.Serializer, None
    ] = None
    query_serializer: serializers.Serializer = None
    manual_parameters: list[openapi.Parameter] = None
    operation_id: str = None
    operation_description: str = None
    operation_summary: str = None
    security: list[dict] = None
    deprecated: bool = None
    responses: dict[
        Union[int, str],
        Union[
            openapi.Schema, openapi.SchemaRef, openapi.Response, serializers.Serializer
        ],
    ] = None
    field_inspectors: list[inspectors.FieldInspector] = None
    filter_inspectors: list[inspectors.FilterInspector] = None
    paginator_inspectors: list[inspectors.PaginatorInspector] = None
    tags: list[str] = None
    extra_overrides: dict = field(default_factory=dict)


@api_view(["GET"])
def stub(request, *args, **kwargs):
    """This is a stub for an endpoint that has not yet been developed."""
    return Response({"error": "This endpoint is not yet developed."})


def documented_api(docs: APIDocs):
    """A decorator that applies a OpenAPI schema to an API method.

    For more information, see the drf-yasg `swagger-auto-schema` docs."""

    def decorator(view_method):
        return swagger_auto_schema(**docs.__dict__)(view_method)

    return decorator
