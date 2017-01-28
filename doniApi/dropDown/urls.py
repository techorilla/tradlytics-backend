from doniApi import *
from django.conf.urls import include, url
from doniApi.dropDown import *

'''
    All Drop Down APIs
'''


urlpatterns = (

    # Business Partner Related API

    url(r'^business_type/$',
        BusinessTypeAPI.as_view(),
        name='Business Partner Basic'),

    url(r'^contact_type/$',
        ContactType.as_view(),
        name='Contact Type Drop Down'),

    url(r'^contract_type/$',
        ContractType.as_view(),
        name='Contract Type Drop Down'),

    url(r'^designation/$',
        Designation.as_view(),
        name='Designation Drop Down'),

    url(r'^product_quality/$',
        ProductQuality.as_view(),
        name='Product quality Drop Down'),

    url(r'^transaction_status/$',
        TransactionStatus.as_view(),
        name='Transaction Status Drop Down')
)
