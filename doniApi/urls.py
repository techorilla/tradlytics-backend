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

    # Product Pricing API

    # Origins API

    url(r'origin/(?P<origin_id>[0-9]+)/$',
        OriginsAPI.as_view(),
        name='Products Origin'),

    url(r'origin/$',
        OriginsAPI.as_view(),
        name='Products Origin'),

    # Product Keyword API

    url(r'keywords/$',
        ProductsKeywordAPI.as_view(),
        name='Products Keywords'),

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


    # Blog Related API

    url(r'blog/tag_list/$',
        TagList.as_view(),
        name='tag-list'),

    url(r'blog/tag_list/(?P<pk>[0-9]+)/$',
        TagDetail.as_view(),
        name='tag-detail'),

    url(r'blog/$',
        BlogList.as_view(),
        name='blog-list'),

    url(r'^(?P<pk>[0-9]+)/$',
        BlogDetail.as_view(),
        name='blog-detail'),

    # Tab Filters Related API

    url(r'tabFilters/list/$',
        TabFiltersAPI.as_view(),
        name='tab-filters'
        ),

    # DropDownRelatedAPI
    url(r'^dropDown/',
        include('doniApi.dropDown.urls'))


)
