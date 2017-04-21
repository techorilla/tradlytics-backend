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
import tldextract


import json


class GetGoogleAccessTokenAPI(APIView):

    permission_classes = (IsAuthenticated, )

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
        }
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
        flow = self.get_tramodity_flow()
        if data.get('code'):
            auth_code = data.get('code')
            credentials = flow.step2_exchange(auth_code)
            token_data = credentials.to_json()
            token_data = json.loads(token_data)
            try:
                business = request.user.profile.business
                access_token = token_data.get('access_token')
                service, http = self.get_service(business, access_token=access_token)
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
    def get_tramodity_flow(cls):
        flow = client.flow_from_clientsecrets(
            settings.GOOGLE_SERVICE_ACCOUNT_JSON,
            scope='https://www.googleapis.com/auth/drive.metadata.readonly',
            redirect_uri=settings.FRONT_END_HOST
        )
        flow.params['access_type'] = 'offline'
        flow.params['include_granted_scopes'] = True
        return flow

    def get_credentials_from_auth_code(self, auth_code):
        return self.flow.step2_exchange()

    @classmethod
    def get_credentials(cls, business, access_token=None):
        if access_token is None:
            token_data = GoogleAnalyticsToken.objects.filter(business=business).order_by("-created")[0].data
            access_token = token_data.get(u'access_token')
        print access_token
        credentials = client.AccessTokenCredentials(access_token, 'my-user-agent/1.0')
        http = httplib2.Http()
        http = credentials.authorize(http)
        return http, credentials

    @classmethod
    def get_service(cls, business, access_token=None):
        http, credentials = cls.get_credentials(business, access_token)
        service = build(cls.API_NAME, cls.API_VERSION, http=http)
        return service, http

    @classmethod
    def verify_account(cls, business, profiles):
        domain = tldextract.extract(business.bp_website).domain
        print domain
        print profiles
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
        traffic_rows = traffic.get('rows')
        traffic_total = traffic.get('totalsForAllResults')
        traffic_total = {
            'newUsers': traffic_total.get('ga:newUsers'),
            'ga:visits': traffic_total.get('ga:visits')
        }

        def map_traffic_row(row):
            row_obj = dict()
            row_obj['date'] = dt.strptime(row[0], '%Y%m%d')
            row_obj['visits'] = row[1]
            row_obj['newUsers'] = row[2]
            return row_obj

        traffic_chart_data = map(map_traffic_row, traffic_rows)

        return {
            'trafficTotal': traffic_total,
            'trafficChartData': traffic_chart_data
        }




