from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class BaseAPI(object):
    ALL_QUERY = 'all'
    DROP_DOWN_QUERY = 'drop_down'

