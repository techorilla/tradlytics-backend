from django.contrib.auth.models import User

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from website.models import GoogleAnalyticsToken
from django.conf import settings
from oauth2client import client
import httplib2
from apiclient.discovery import build
from apiclient.http import BatchHttpRequest
import tldextract
from doniApi.apiImports import Response, APIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from datetime import datetime as dt
from pycountry import countries
import tldextract


import json


class GetGoogleAccessTokenAPI(APIView):

    permission_classes = (IsAuthenticated, )

    AUTHORIZATION_SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
    REDIRECT_PREFIX = "http://tramodity.com"
    API_ENDPOINT = "https://www.googleapis.com/analytics/v3"
    API_NAME = "analytics"
    API_VERSION = "v3"

    DATA_CONFIGS = {
        'traffic_30': {
            'start_date': '30daysAgo',
            'end_date': 'today',
            'metrics': 'ga:visits,ga:newUsers',
            'dimensions': 'ga:date',
        },
        'country_traffic_total_30': {
            'start_date': '30daysAgo',
            'end_date': 'today',
            'dimensions': 'ga:country',
            'metrics': 'ga:sessions',
            'sort': '-ga:sessions'
        },
        'cardData':{
            'start_date': '30daysAgo',
            'end_date': 'today',
            'metrics': 'ga:hits,ga:avgSessionDuration,ga:bounceRate, ga:sessions, ga:pageViews',
            'dimensions': 'ga:date',
        },

    }


    testing_token = {
        u'status': {u'google_logged_in': False, u'signed_in': False, u'method': None},
        u'domain': u'riccado.co.uk', u'code': u'4/FfCOjCnnWKypExrjUMxpXNFY3eiW6zhPRsXXL6Q3AG0',
        u'expires_in': u'86400',
        u'expires_at': u'1478345540',
        u'g-oauth-window': {},
        u'state': u'', u'response_type': u'code',
        u'client_id': u'652996843064-si7cgafsq10i6vrce8l31hi3tk1cserh.apps.googleusercontent.com',
        u'issued_at': u'1478259140',
        u'scope': u'https://www.googleapis.com/auth/analytics.readonly'
    }

    def post(self, request, *args, **kwargs):
        data = request.data
        origin = request.META.get('HTTP_ORIGIN')
        flow = self.get_tramodity_flow(origin)
        if data.get('code'):
            auth_code = data.get('code')
            credentials = flow.step2_exchange(auth_code)
            token_data = credentials.to_json()
            try:
                business = request.user.profile.business
                service, http = self.get_service(credentials=credentials)
                profiles = self.get_profiles(service)
                valid_profile = self.verify_account(business, profiles)
                if valid_profile:
                    self.save_google_analytics_token(business, token_data, request.user)
                    return Response({
                        'success': True,
                        'message': 'Google Analytics account of %s connected successfully!' % request.user.username
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'success': False,
                        'message': 'You account does not contain profile for %s.' % business.bp_website
                    })
            except Exception, e:

                return Response({
                    'success': False,
                    'message':  str(e)
                }, status=status.HTTP_200_OK)

        else:
            return Response({
                'success': False,
                'message': 'Unable to get access token'
            })





    @classmethod
    def save_google_analytics_token(cls, business, token_data, user):
        # delete existing token if any
        existing_token = GoogleAnalyticsToken.objects.filter(business=business)
        existing_token.delete()
        ga_token = GoogleAnalyticsToken()
        ga_token.business = business
        ga_token.data = token_data
        ga_token.user = user
        ga_token.save()

    @classmethod
    def get_tramodity_flow(cls, base_url):
        flow = client.flow_from_clientsecrets(
            settings.GOOGLE_ANALYTICS_CLIENT_SECRETS,
            scope=cls.AUTHORIZATION_SCOPE,
            redirect_uri=base_url
        )
        flow.params['access_type'] = 'offline'
        flow.params['include_granted_scopes'] = True
        return flow

    def get_credentials_from_auth_code(self, auth_code):
        return self.flow.step2_exchange()

    @classmethod
    def get_credentials(cls, business):
        token_data = GoogleAnalyticsToken.objects.filter(business=business).order_by("-created")[0].data
        credentials = client.OAuth2Credentials.from_json(token_data)
        return credentials


    def get_service(self, business=None, credentials=None):
        if credentials is None:
            credentials = self.get_credentials(business)
        http = credentials.authorize(http=httplib2.Http())
        service = build(self.API_NAME, self.API_VERSION, http=http)
        return service, http

    @classmethod
    def verify_account(cls, business, profiles):
        domain = tldextract.extract(business.bp_website).domain
        profile_domains = [tldextract.extract(profile.get('websiteUrl')).domain for profile in profiles]
        return domain in profile_domains


    @classmethod
    def get_profiles(cls, service):
        # Get a list of all Google Analytics accounts for the authorized user.
        accounts = service.management().accounts().list().execute()
        if accounts.get('items'):
            # Get the first Google Analytics account.
            account = accounts.get('items')[0].get('id')
            # Get a list of all the properties for the first account.
            properties = service.management().webproperties().list(
                accountId=account).execute()
            if properties.get('items'):
                # Get the first property id.
                property = properties.get('items')[0].get('id')

                # Get a list of all views (profiles) for the first property.
                profiles = service.management().profiles().list(
                    accountId=account,
                    webPropertyId=property).execute()

                if profiles.get('items'):
                    # return the first view (profile) id.
                    return profiles.get('items')
        return []

    def get_data_from_google_analytics(self, business):
        service, http = self.get_service(business)
        data = {}

        def get_data_callback(request_id, response, exception):
            data[request_id] = response

        batch = BatchHttpRequest(callback=get_data_callback)
        for section in self.DATA_CONFIGS.keys():
            batch.add(service.data().ga().get(
                ids='ga:'+settings.GOOGLE_ANALYTICS_PROFILE_ID,
                start_date=self.DATA_CONFIGS.get(section, {}).get('start_date'),
                end_date=self.DATA_CONFIGS.get(section, {}).get('end_date'),
                metrics=self.DATA_CONFIGS.get(section, {}).get('metrics'),
                dimensions=self.DATA_CONFIGS.get(section, {}).get('dimensions'),
                filters=self.DATA_CONFIGS.get(section, {}).get('filters')
            ), request_id=section)
        batch.execute(http=http)
        return self.prepare_data_for_dashboard(data)

    def prepare_data_for_dashboard(self,data):
        traffic = data.get('traffic_30')
        country_traffic = data.get('country_traffic_total_30').get('rows')
        card_data = data.get('cardData')
        cards_total_data = card_data.get('totalsForAllResults')
        traffic_rows = traffic.get('rows')
        traffic_total = traffic.get('totalsForAllResults')
        traffic_total = {
            'newUsers': traffic_total.get('ga:newUsers'),
            'ga:visits': traffic_total.get('ga:visits')
        }

        cards_total_data = {
            'newUsers': traffic_total.get('ga:newUsers'),
            'visits': traffic_total.get('ga:visits'),
            'avgSessionDuration': float(cards_total_data.get('ga:avgSessionDuration')),
            'pageViews': int(cards_total_data.get('ga:pageViews')),
            'bounceRate': float(cards_total_data.get('ga:bounceRate')),
            'sessions': int(cards_total_data.get('ga:sessions')),
            'hits': int(cards_total_data.get('ga:hits'))
        }

        def map_country_traffic(row):
            row_obj = dict()
            country = countries.get(name=row[0])
            row_obj['code'] = country.alpha_2
            row_obj['name'] = row[0]
            row_obj['value'] = row[1]
            return row_obj

        def map_traffic_row(row):
            row_obj = dict()
            row_obj['date'] = dt.strptime(row[0], '%Y%m%d')
            row_obj['visits'] = int(row[1])
            row_obj['newUsers'] = int(row[2])
            return row_obj

        traffic_chart_data = map(map_traffic_row, traffic_rows)
        traffic_country_chart_data = map(map_country_traffic, country_traffic)

        return {
            'trafficTotal': traffic_total,
            'trafficChartData': traffic_chart_data,
            'trafficCountryChartData': traffic_country_chart_data,
            'cardsTotalData': cards_total_data
        }




