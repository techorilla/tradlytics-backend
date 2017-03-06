from doniApi import *
from django.conf.urls import include, url

'''
    All Data API for Doni Group
'''

urlpatterns = (

    # User Related API

    url(r'user/$',
        User.as_view(),
        name='User'),

    url(r'user/(?P<user_id>[0-9]+)/profilePic/$',
        UserProfilePicAPI.as_view(),
        name='User'),

    # Business Partner Related API

    url(r'bp_partner/(?P<bp_id>[a-zA-Z0-9.@_-]+)/basic/$',
        BpBasicAPI.as_view(),
        name='Business Partner Basic'),

    url(r'bp_partner/(?P<bp_id>[a-zA-Z0-9.@_-]+)/bank/(?P<bank_id>[a-zA-Z0-9.@_-]+)/$',
        BpContactNumberAPI.as_view(),
        name='Business Partner Basic'),

    url(r'bp_partner/(?P<bp_id>[a-zA-Z0-9.@_-]+)/contact_number/(?P<cn_id>[a-zA-Z0-9.@_-]+)/$',
        BpContactNumberAPI.as_view(),
        name='Business Partner Contact Number'),

    url(r'bp_partner/(?P<bp_id>[a-zA-Z0-9.@_-]+)/contact_person/(?P<cp_id>[a-zA-Z0-9.@_-]+)/$',
        BpContactNumberAPI.as_view(),
        name='Business Partner Person'),

    url(r'bp_partner/(?P<bp_id>[a-zA-Z0-9.@_-]+)/product/(?P<product_id>[a-zA-Z0-9.@_-]+)/$',
        BpProductsAPI.as_view(),
        name='Business Partner Products'),

    url(r'bp_partner/(?P<bp_id>[a-zA-Z0-9.@_-]+)/location/$',
        BpLocationAPI.as_view(),
        name='Business Partner Locations'),

    # Transaction Related API

    url(r'transactions/basic/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionBasicAPI.as_view(),
        name='Transaction Basic'),

    url(r'transactions/commission/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionCommissionAPI.as_view(),
        name='Transaction Commission'),

    url(r'transactions/contract/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionContractAPI.as_view(),
        name='Transaction Contract'),

    url(r'transactions/document/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionNoteAPI.as_view(),
        name='Transaction Documents'),

    url(r'transactions/note/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionBasicAPI.as_view(),
        name='Transaction Notes'),

    url(r'transactions/secondary/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionSecondaryAPI.as_view(),
        name='Transaction Secondary'),

    url(r'transactions/(?P<tr_id>[a-zA-Z0-9.@_-]+)/status/$',
        TransactionBasicAPI.as_view(),
        name='Transaction Status'),

    url(r'transactions/(?P<tr_id>[a-zA-Z0-9.@_-]+)/shipment/$',
        TransactionShipmentAPI.as_view(),
        name='Transaction Shipment'),

    # Reports Related API

    # Manifest Related API

    # Price Market API

    url(r'pricing/price_market/$',
        PricingMarketAPI.as_view(),
        name='Pricing_Market_API'
        ),

    # Product Items Pricing API

    url(r'pricing/product_item/$',
        ProductItemPricingAPI.as_view(),
        name='Product_Item_Pricing_API'),

    # Product Pricing API

    url(r'pricing/(?P<product_id>[0-9]+)/$',
        WebsitePricingAPI.as_view(),
        name='website_pricing_api'
        ),

    # Product Keyword API

    url(r'product/category',
        ProductsCategoryAPI.as_view(),
        name='Product_Category_API'),

    url(r'product/keywords/$',
        ProductsKeywordAPI.as_view(),
        name='Products Keywords API'),

    url(r'product/keywords/(?P<product_id>[0-9]+)/$',
        ProductsKeywordAPI.as_view(),
        name='Products Keywords'),

    url(r'keywords/(?P<keyword_id>[0-9]+)/$',
        ProductsKeywordAPI.as_view(),
        name='Products Keywords'),

    # Product API

    # Product Image API

    url(r'product/image/$',
        ProductsImageAPI.as_view(),
        name='Products Image'),

    url(r'product/(?P<product_id>[0-9]+)/image/$',
        ProductsImageAPI.as_view(),
        name='Products Image'),

    # Product Related API

    url(r'product/$',
        ProductsAPI.as_view(),
        name='Products'),

    url(r'^product_item/$',
        ProductItemAPI.as_view(),
        name='Products_Item_API'),


    # DropDownRelatedAPI
    url(r'^dropDown/',
        include('doniApi.dropDown.urls')),

    # Website Related APIs
    url(r'^contact_us/$',  ContactUsAPI.as_view(), {"public_api": True}, name='website-contact-us', ),

    url(r'^newsletter/$', NewsLetterAPI.as_view(), name='website-newsletter')


)
