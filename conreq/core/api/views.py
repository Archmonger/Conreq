import json

from conreq.core.arrs.sonarr_radarr import ArrManager
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.user_requests.helpers import radarr_request, sonarr_request
from django.contrib.auth import authenticate, login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


# Create your views here.
class RequestTv(APIView):
    """Request a TV show by TMDB ID."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = {"success": True, "detail": None}

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "seasons": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                "episodes": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "success": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                    ),
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                },
            ),
        },
    )
    def post(self, request, tmdb_id):
        """Request a TV show by TMDB ID. Optionally, you can request specific seasons or episodes."""
        content_manager = ArrManager()
        content_discovery = TmdbDiscovery()
        tvdb_id = content_discovery.get_external_ids(tmdb_id, "tv")
        request_parameters = json.loads(request.body.decode("utf-8"))

        # Request the show by the TVDB ID
        if tvdb_id:
            sonarr_request(
                tvdb_id["tvdb_id"],
                tmdb_id,
                request,
                request_parameters,
                content_manager,
                content_discovery,
            )
            return Response(self.msg)
        return Response({"success": False, "detail": "Could not determine TVDB ID."})


class RequestMovie(APIView):
    """Request a movie by TMDB ID."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = {"success": True, "detail": None}

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "success": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                    ),
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                },
            ),
        },
    )
    def post(self, request, tmdb_id):
        """Request a movie by TMDB ID."""
        content_manager = ArrManager()
        content_discovery = TmdbDiscovery()

        # Request the show by the TMDB ID
        radarr_request(
            tmdb_id,
            request,
            content_manager,
            content_discovery,
        )
        return Response(self.msg)


class LocalAuthentication(APIView):
    """Sign in to an account."""

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                    ),
                    "last_login": openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                    "is_superuser": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                    ),
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                    "first_name": openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                    "last_name": openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                    "is_staff": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                    ),
                    "is_active": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                    ),
                    "date_joined": openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                    "groups": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_INTEGER),
                    ),
                    "user_permissions": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_INTEGER),
                    ),
                    "profile": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "language": openapi.Schema(
                                type=openapi.TYPE_STRING,
                            ),
                            "externally_authenticated": openapi.Schema(
                                type=openapi.TYPE_BOOLEAN,
                            ),
                        },
                    ),
                    "auth_token": openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                },
            ),
        },
    )
    def post(self, request):
        """Authenticate a session using a `username` and `password`. Requires CSRF tokens on all further insecure requests (POST, PUT, DELETE, PATCH)."""
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        else:
            pass


@api_view(["GET"])
def stub(request):
    """This is a stub for an endpoint that has not yet been developed."""
    return Response({})
