from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def stub(request, *args, **kwargs):
    """This is a stub for an endpoint that has not yet been developed."""
    return Response({})
