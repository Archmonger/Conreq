import json

from conreq.core.arrs.sonarr_radarr import ArrManager
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class RequestTv(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = {"success": True, "message": None}

    def get(self, request):
        return Response(self.msg)

    def post(self, request):
        return Response(self.msg)


@api_view(["GET", "POST"])
def request_movie(request):
    return Response({})
