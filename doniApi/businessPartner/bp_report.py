from doniApi.apiImports import Response, GenericAPIView, status
from doniCore.utils import Utilities
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import BpBasic, BusinessType
import json, os
from datetime import datetime as dt
from doniCore import cache_results
from doniCore.cache import cache, doni_redis
from django.conf import settings



class BusinessReportAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        business_report = dict()
        return Response({
            'success': True,
            'businessReport': business_report
        })


