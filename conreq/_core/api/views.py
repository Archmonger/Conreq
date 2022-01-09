from django.contrib.auth import authenticate, login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from conreq._core.api.serializers import UserSerializer


# TODO: Create some API views.
class LocalAuthentication(APIView):
    """Sign in to an account."""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                ),
            },
        ),
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
        """Authenticate a session using a `username` and `password`.
        Requires CSRF tokens on all further insecure requests (POST, PUT, DELETE, PATCH)."""
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response(None)
