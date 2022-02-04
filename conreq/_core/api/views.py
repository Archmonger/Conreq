from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView

from conreq._core.api.serializers import UserSerializer


# TODO: Create some API views.
class LocalAuthentication(APIView):
    """Sign in to an account."""

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
