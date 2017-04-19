from django.conf import settings
import requests
import json
import urllib
import re
import time
from django.conf import settings


class GooglePlaces(object):

    GOOGLE_API_KEY = settings.GOOGLE_API_KEY

    def get_place(self, place_id, region):

        params = {
            'placeid': place_id,
            'region': region,
            'key': self.GOOGLE_API_KEY,
        }
        a=requests.get('https://maps.googleapis.com/maps/api/place/details/json', params=params)
        if a.json()['status'] == 'OVER_QUERY_LIMIT':
            print 'OVER_QUERY_LIMIT'
            return 'OVER_QUERY_LIMIT'
        elif a.json()['status'] == 'NOT_FOUND':
            print 'NOT_FOUND'
            return 'NOT_FOUND'
        else:
            return a.json()['result']

    def search_text(self, name, uk=False):
        time.sleep(2)
        params = {
            'query': name,
            'key': self.GOOGLE_API_KEY
        }
        if not uk:
            params['region'] = 'uk'
        try:
            a = requests.get("https://maps.googleapis.com/maps/api/place/" + \
                             "textsearch/json", params=params)
            if a.json()['status'] == 'OVER_QUERY_LIMIT':
                return 'OVER_QUERY_LIMIT'
            else:
                return a.json()['results']
        except Exception, e:
            print "Searching Google Place Exception: %s" % e
            pass

