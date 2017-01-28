import requests
from .etlManager import *
from doniServer.models import *
from django.utils import timezone
from django.contrib.auth.models import User


class EtlOrigin(EtlManager):
    GET_ALL_ORIGIN_URL = 'http://54.191.252.114:44200/getAllOrigin'
    MODEL = Origin

    @staticmethod
    def get_all_origin():
        data = requests.get(url=EtlOrigin.GET_ALL_ORIGIN_URL, headers=EtlManager.HEADERS)
        return data.json()

    def migrate_origins(self):
        self.MODEL.objects.all().delete()
        all_origins = self.get_all_origin().get('origins', [])
        map(self.store_origin_in_database, all_origins)
        return all_origins

    @staticmethod
    def store_origin_in_database(origin):
        print origin
        origin_id = origin.get('origin_id')
        origin_name = origin.get('origin_name')
        created_by = User.objects.get(email='immadimtiaz@gmail.com')
        Origin.objects.create(id=origin_id, name=origin_name,
                              created_at=timezone.now(), created_by=created_by, updated_at=None, )







