from .api import *
from django.conf.urls import include, url

urlpatterns = (

    url("^trade/$", LocalTradeAPI.as_view(), name="local_trade"),
    url("^trade/status/$", LocalTradeStatusAPI.as_view(), name="local_trade"),
    url("^trade/list/$", LocalTradeListAPI.as_view(), name="local_trade"),
    url("^dashboard/$", LocalTradeDashboardAPI.as_view(), name="local_trade"),
    url("^delivery_slip/$", LocalTradeDeliverySlipAPI.as_view(), name="delivery_slip")

)