from django.conf import settings

from django.conf import settings
from doniApi.authentication.google_analytics_token import *


class GetGoogleAnalyticsData(object):

    def __init__(self):
        self.API_KEY = settings.GOOGLE_API_KEY

    def run_routine(self, business):
        obj = GetGoogleAccessTokenAPI()
        obj.get_data_from_google_analytics(business)
        return None


