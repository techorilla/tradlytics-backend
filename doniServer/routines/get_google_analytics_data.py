from django.conf import settings

from django.conf import settings
from oauth2client.service_account import ServiceAccountCredentials




class GetGoogleAnalyticsData(object):
    API_ENDPOINT = "https://www.googleapis.com/analytics/v3"
    API_NAME = "analytics"
    API_VERSION = "v3"
    SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']

    DATA_CONFIGS = {
        'total': {
            'metrics': 'ga:visits',
            'dimensions': 'ga:yearMonth'
        },
        'social': {
            'metrics': 'ga:visits',
            'dimensions': 'ga:socialNetwork, ga:yearMonth',
            'filters': 'ga:socialNetwork!=(not set);ga:socialNetwork!=(none)',
        },
        'direct': {
            'metrics': 'ga:visits',
            'dimensions': 'ga:yearMonth',
            'filters': 'ga:sourceMedium=@(direct)',
        },
        'email': {
            'metrics': 'ga:visits',
            'dimensions': 'ga:yearMonth',
            'filters': 'ga:sourceMedium=@/ email'
        },
        'search': {
            'metrics': 'ga:visits',
            'dimensions': 'ga:yearMonth',
            'filters': 'ga:medium==organic'
        },
        'referrals': {
            'metrics': 'ga:visits',
            'dimensions': 'ga:yearMonth',
            'filters': 'ga:medium==referral'
        },
        'paid_referrals': {
            'metrics': 'ga:visits',
            'dimensions': 'ga:yearMonth',
            'filters': 'ga:medium==cpa,ga:medium==cpc,ga:medium==cpm,ga:medium==cpp,ga:medium==cpv,ga:medium==ppc',
        },
        'website_engagement': {
            'metrics': 'ga:hits,ga:avgSessionDuration,ga:bounceRate, ga:sessions',
            'dimensions': 'ga:yearMonth'
        },
        'country_traffic':{
            'dimensions': 'ga:country, ga:yearMonth',
            'metrics': 'ga:sessions',
            'sort': '-ga:sessions'
        }

    }

    def __init__(self):
        self.API_KEY = settings.GOOGLE_API_KEY

    def run_routine(self):
        return None


