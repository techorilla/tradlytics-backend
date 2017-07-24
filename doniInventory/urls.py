from .api import *
from django.conf.urls import include, url

urlpatterns = (

    url("^dashboard/$", InventoryDashboardAPI.as_view(), name="inventory_dashboard"),
    url(r"^warehouse/$", WarehouseAPI.as_view(), name="warehouse"),
    url(r"^warehouse/list/$", WarehouseListAPI.as_view(), name="warehouse_list"),
    url(r"^transaction/$", InventoryTransactionAPI.as_view(), name="inventory_transactions"),
    url(r"^warehouse_rent/$", WarehouseRentAPI.as_view(), name="warehouse_rent"),

)