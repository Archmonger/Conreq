from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    _SerializerType,
    extend_schema,
)
from rest_framework.decorators import api_view
from rest_framework.fields import empty
from rest_framework.response import Response


@dataclass
class APIDocs:
    """Information that can be passed into an `documented_api`.
    See drf-spectacular docs for more information."""

    # pylint: disable=too-many-instance-attributes

    operation_id: Optional[str] = None
    """replaces the auto-generated operation_id. make sure there
        are no naming collisions."""

    parameters: Optional[List[Union[OpenApiParameter, _SerializerType]]] = None
    """list of additional or replacement parameters added to the
        auto-discovered fields."""

    responses: Any = empty
    """replaces the discovered Serializer. Takes a variety of
        inputs that can be used individually or combined

        - ``Serializer`` class
        - ``Serializer`` instance (e.g. ``Serializer(many=True)`` for listings)
        - basic types or instances of ``OpenApiTypes``
        - :class:`.OpenApiResponse` for bundling any of the other choices together with
            either a dedicated response description and/or examples.
        - :class:`.PolymorphicProxySerializer` for signaling that
            the operation may yield data from different serializers depending
            on the circumstances.
        - ``dict`` with status codes as keys and one of the above as values.
            Additionally in this case, it is also possible to provide a raw schema dict
            as value.
        - ``dict`` with tuples (status_code, media_type) as keys and one of the above
            as values. Additionally in this case, it is also possible to provide a raw
            schema dict as value."""

    request: Any = empty
    """replaces the discovered ``Serializer``. Takes a variety of inputs

        - ``Serializer`` class/instance
        - basic types or instances of ``OpenApiTypes``
        - :class:`.PolymorphicProxySerializer` for signaling that the operation
          accepts a set of different types of objects.
        - ``dict`` with media_type as keys and one of the above as values. Additionally in
          this case, it is also possible to provide a raw schema dict as value."""

    auth: Optional[List[str]] = None
    """replace discovered auth with explicit list of auth methods"""

    description: Optional[str] = None
    """replaces discovered doc strings"""

    summary: Optional[str] = None
    """an optional short summary of the description"""

    deprecated: Optional[bool] = None
    """mark operation as deprecated"""

    tags: Optional[List[str]] = None
    """override default list of tags"""

    filters: Optional[bool] = None
    """ignore list detection and forcefully enable/disable filter discovery"""

    exclude: bool = False
    """set True to exclude operation from schema"""

    operation: Optional[Dict] = None
    """manually override what auto-discovery would generate. you must
        provide a OpenAPI3-compliant dictionary that gets directly translated to YAML."""

    methods: Optional[List[str]] = None
    """scope extend_schema to specific methods. matches all by default."""

    versions: Optional[List[str]] = None
    """scope extend_schema to specific API version. matches all by default."""

    examples: Optional[List[OpenApiExample]] = None
    """attach request/response examples to the operation"""

    extensions: Optional[Dict[str, Any]] = None
    """specification extensions, e.g. ``x-badges``, ``x-code-samples``, etc."""


@api_view(["GET"])
def stub(*_, **__):
    """This is a stub for an endpoint that has not yet been developed."""
    return Response({"error": "This endpoint is not yet developed."})


def extend_docs(docs: APIDocs):
    """A decorator that applies a OpenAPI schema to an API method.

    For more information, see the drf-spectacular `extend_schema` docs."""

    def decorator(view_method):
        return extend_schema(**docs.__dict__)(view_method)

    return decorator
