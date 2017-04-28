from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniApi.authentication.google_analytics_token import *
import dateutil.parser
from datetime import datetime as dt
import pytz
import json

class WebsiteDashboardAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        business = user.profile.business
        googe_analytics_connected = business.ga_token.exists()
        if googe_analytics_connected:
            ga_token = business.ga_token.all().order_by('-created')[0]
            ga_token_data = json.loads(ga_token.data)
            expiry = ga_token_data.get('token_expiry')
            expiry_date = dateutil.parser.parse(expiry)
            expiry_date = expiry_date.replace(tzinfo=pytz.UTC)
            is_expired = (dt.now(pytz.utc) > expiry_date)
            if is_expired:
                ga_token.delete()
                googe_analytics_connected = False
        dashboard_data = dict()
        dashboard_data['googleAnalyticsConnected'] = googe_analytics_connected
        if googe_analytics_connected and not is_expired:
            ga = GetGoogleAccessTokenAPI()
            data = ga.get_data_from_google_analytics(business)
            dashboard_data['data'] = data
        return Response({
            'success': True,
            'dashboardData': dashboard_data
        }, status=status.HTTP_200_OK)

