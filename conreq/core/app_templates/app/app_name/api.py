"""
API endpoint registration for {{ verbose_name }}.

See more information in the Conreq Register API docs.
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from conreq.app.register import api