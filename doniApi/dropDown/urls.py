from doniApi import *
from django.conf.urls import include, url
from doniApi.dropDown import *

'''
    All Drop Down APIs
'''


urlpatterns = (

    # Business Partner Related API

    url(r'^transaction/$',
        TransactionDropDownAPI.as_view(),
        name='International Transaction Type'),

    url(r'^localTransaction/$',
        LocalTransactionDropDownAPI.as_view(),
        name='Local Transaction'),

    url(r'^commission_type/$',
        CommissionTypeAPI.as_view(),
        name='Commission Type'),

    url(r'^packaging/$',
        PackagingAPI.as_view(),
        name='Business Partner Basic'),

    url(r'^warehouses/$',
        WarehouseDDAPI.as_view(),
        name='Warehouses'),

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

    url(r'^product_keywords/$',
        ProductKeywords.as_view(),
        name='Product quality Drop Down'),

    url(r'^transaction_status/$',
        TransactionStatus.as_view(),
        name='Transaction Status Drop Down'),

    url(r'^product_drop_down/$',
        ProductDDAPI.as_view(),
        name='Product Drop Down'
        ),

    url(r'^product_origin/$',
        ProductOriginDDAPI.as_view(),
        name='Product Origin Drop Down'
        ),

    url(r'currency/$',
        CurrencyDDAPI.as_view(),
        name='Currency'
        ),

    url(r'^product_category/$',
        ProductCategoryDDAPI.as_view(),
        name='Product_Category_Drop_Down'),

    url(r'^product_item/$',
        ProductItemDDAPI.as_view(),
        name='Product_Items_Drop_Down'),

    url(r'^price_market/$',
        PriceMarketDDAPI.as_view(),
        name='Price_Market_Drop_Down'),

    url(r'country/$',
        CountryAPI.as_view(),
        name='Countries_API'),

    url(r'region/$',
        RegionAPI.as_view(),
        name='Countries_API'),

    url(r'city/$',
        CityAPI.as_view(),
        name='Countries_API'),

    url(r'shipment_month/$',
        ShipmentMonthDDAPI.as_view(),
        name='Shipement_Month_API'
        ),

    url(r'price_metric/$',
        PriceMetricDDAPI.as_view(),
        name='Shipement_Month_API'
        ),

    url(r'business/$',
        BusinessDropDownAPI.as_view(),
        name='Business_Drop_Down_API'),

    url(r'ports/$',
        ShippingPortDDAPI.as_view(),
        name='Business_Drop_Down_API'),

    url(r'shipping_line/$',
        ShippingLineDDAPI.as_view(),
        name='Business_Drop_Down_API'),

    url(r'vessel/$',
        ShippingVesselDDAPI.as_view(),
        name='Business_Drop_Down_API'),


)
