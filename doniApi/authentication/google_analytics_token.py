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



class GetGoogleAccessTokenAPI(GenericAPIView, IsAuthenticated):

    permission_classes = (IsAuthenticated, )

    API_ENDPOINT = "https://www.googleapis.com/analytics/v3"
    API_NAME = "analytics"
    API_VERSION = "v3"

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
        try:
            business = request.user.profile.business
            credentials, success, urls = self.connect_google_analytics_for_token(business, request.data['code'])
            return Response({'success': success, 'urls': urls})
        except Exception, e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)

    @classmethod
    def connect_google_analytics_for_token(cls, business, token_details=None):
        credentials, success, urls = cls.get_and_save_credentials_from_code(token_details, business)
        log.info(credentials, success, urls)
        for url in urls:
            url_business = Business.objects.get(url=url)
            get_google_analytics_data(url_business)
        return credentials, success, urls

    @classmethod
    def get_and_save_credentials_from_code(self, auth_code, business=None):
        try:
            if business:
                self.get_tramodity_flow()
            credentials = self.flow.step2_exchange(auth_code)
            business_found = False
            urls = []
            service, http = self.get_service(credentials=credentials)
            profiles = self.get_profiles(service)
            for profile in profiles:
                websiteurl = profile.get('websiteUrl')
                domain = extract_domain(websiteurl)
                urls.append(domain)
                new_business, created = Business.objects.get_or_create(
                    url=domain)
                token, created = GoogleAnalyticsToken.objects.get_or_create(
                    business=new_business)
                token.data = credentials.to_json()
                token.save()
                if business.url == domain:
                    business_found = True
            return credentials, business_found, urls
        except Exception, e:
            log.exception("exeption while grabbing credentials..: %s" % e)
            return None, business_found, urls


    @classmethod
    def get_tramodity_flow(cls):
        flow = client.flow_from_clientsecrets(
            settings.GOOGLE_SERVICE_ACCOUNT_JSON,
            scope='https://www.googleapis.com/auth/drive.metadata.readonly',
            redirect_uri='http://www.example.com/oauth2callback')
        flow.params['access_type'] = 'offline'
        flow.params['include_granted_scopes'] = True
        return flow

    def generate_oauth_url(self, flow):
        flow = self.get_tramodity_flow()
        auth_uri = flow.step1_get_authorize_url()
        return auth_uri

    @classmethod
    def get_service(cls, business=None, credentials=None):
        if credentials is None:
            credentials = cls.get_credentials(business)
        http = credentials.authorize(http=httplib2.Http())
        service = build(cls.API_NAME, cls.API_VERSION, http=http)
        return service, http

    @classmethod
    def get_credentials(cls, business):
        return client.OAuth2Credentials.from_json(
            GoogleAnalyticsToken.objects.filter(
                business=business).order_by("-created")[0].data)

    def get_profiles(self, service):
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

    def get_data_from_google_analytics(self):
        service, http = self.get_service()

        start_day = '1daysAgo'
        end_day = 'today'
        data = {}

        def get_data_callback(request_id, response, exception):
            print response, exception
            data[request_id] = response

        batch = BatchHttpRequest(callback=get_data_callback)
        for section in self.DATA_CONFIGS.keys():
            batch.add(service.data().ga().get(
                ids='ga:'+settings.GOOGLE_ANALYTICS_PROFILE_ID,
                start_date=start_day,
                end_date=end_day,
                metrics=self.DATA_CONFIGS.get(section, {}).get('metrics'),
                dimensions=self.DATA_CONFIGS.get(section, {}).get('dimensions'),
                filters=self.DATA_CONFIGS.get(section, {}).get('filters')
            ), request_id=section)
        batch.execute(http=http)
        return data
