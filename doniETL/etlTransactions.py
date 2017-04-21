import requests
from .etlManager import *
from doniServer.models import *
from django.utils import timezone
from django.contrib.auth.models import User


class EtlTransactions(EtlManager):
    GET_ALL_TRANSACTIONS = 'http://54.191.252.114:44200/getTransactionTableOnDateRange'
    GET_SINGLE_TRANSACTION = 'http://54.191.252.114:44200/getSingleTransaction?id=1573'
    MODEL = Origin

    @staticmethod
    def get_all_transaction_id():
        params = {
            'startDate': '2012-12-01',
            'endDate': '2016-12-30'
        }
        data = requests.get(url=EtlTransactions.GET_ALL_TRANSACTIONS, headers=EtlManager.HEADERS, params=params)
        all_transactions = data.json()
        return sorted([tran.get('tr_transactionID') for tran in all_transactions])

    def migrate_transactions(self):
        return None

    @staticmethod
    def store_transaction_in_database(tr_id):

        return None







