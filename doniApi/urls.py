from doniApi import *
from django.conf.urls import include, url

from doniApi.authentication.Login import LoginAPI
from doniApi.authentication.Logout import LogOutAPI


'''
    All Data API for Doni Group
'''

urlpatterns = (
    url(r"login/$", LoginAPI.as_view(), {"public_api": True}, name="login"),
    url(r"logout/$", LogOutAPI.as_view(), name="logout"),

    url(r"^auth/google_analytics/$", GetGoogleAccessTokenAPI.as_view(), name='Google_Access_Token'),

    url(r'^dashboard/$', MainDashboardAPI.as_view(), name='Main_Dashboard_API'),

    url(r'^dashboard/search_top/$', PageTopSearchAPI.as_view(), name='Page_Top_API'),

    url(r'website/dashboard/$', WebsiteDashboardAPI.as_view(), name='Website_Dashboard_API'),

    url(r'^website/research/display/$', BlogDisplayAPI.as_view(), name='Blogs_API'),

    url(r'^website/research/$', BlogAPI.as_view(), name='Blogs_API'),

    url(r'^website/research/(?P<research_id>[0-9]+)/$', BlogAPI.as_view(), name='Blogs_API'),

    url(r'website/research_tags', BlogTagAPI.as_view(), name='BlogTagAPI'),

    # User Related API

    url(r'^user/changePassword/$',
        ChangePassword.as_view(),
        name='Change_Password'),

    url(r'user/$',
        User.as_view(),
        name='User'),

    url(r'user/(?P<user_id>[0-9]+)/profilePic/$',
        UserProfilePicAPI.as_view(),
        name='User'),

    # Business Partner Related API

    url(r'business/self/$',
        BusinessSettingsAPI.as_view(),
        name='Self_Business'),

    url(r'business/list/$',
        BusinessListAPI.as_view(),
        name='Business List'),

    url(r'business/basic/$',
        BpBasicAPI.as_view(),
        name='Business Partner Basic'),

    url(r'business/basic/(?P<bp_id>[a-zA-Z0-9.@_-]+)/$',
        BpBasicAPI.as_view(),
        name='Business Partner Basic'),

    url('business/location/$',
        BpLocationAPI.as_view(),
        name='Business Location API'),

    url('business/contact_person/$',
        BpContactPersonAPI.as_view(),
        name='Business Contact Person API'),

    url('business/contact_number/$',
        BpContactNumberAPI.as_view(),
        name='Business Contact Number API'),

    url('business/bank/$',
        BpBankAPI.as_view(),
        name='Business Bank API'),

    # Transaction Related API

    url(r'transactions/list/$',
        TransactionListAPI.as_view(),
        name='Transaction List'),

    url(r'transactions/washout/$',
        TransactionWashoutAPI.as_view(),
        name='Transaction Washout'),

    url(r'transactions/completeStatus/$',
        TransactionCompleteStatusAPI.as_view(),
        name='Transaction List'),

    url(r'transactions/shipmentStatus/$',
        TransactionShipmentStatusAPI.as_view(),
        name='Transaction List'),

    url(r'transactions/approbation_received_info/$',
        ShipmentApprobationReceivedInfoAPI.as_view(),
        name='Transaction Approbation Recieved Info'),

    url(r'transactions/arrived_at_port_info/$',
        ShipmentArrivedAtPortInfoAPI.as_view(),
        name='Transaction Arrived Info'),

    url(r'transactions/shipped_info/$',
        ShipmentShippedInfoAPI.as_view(),
        name='Transaction Shipment Info'),

    url(r'transactions/not_shipped_info/$',
        ShipmentNotShippedInfoAPI.as_view(),
        name='Transaction Not Shipped Info'),

    url(r'transaction/list/dropdown/$',
        TransactionDropDownAPI.as_view(),
        name='Transaction List Dropdown'),

    url(r'transactions/basic/$',
        TransactionBasicAPI.as_view(),
        name='Transaction Basic'),

    url(r'transactions/basic/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionBasicAPI.as_view(),
        name='Transaction Basic'),

    url(r'transactions/note/(?P<tr_id>[a-zA-Z0-9.@_-]+)/(?P<note_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionNoteAPI.as_view(),
        name='Transaction Basic'),

    url(r'transactions/note/$',
        TransactionNoteAPI.as_view(),
        name='Transaction Notes'),

    url(r'transactions/note/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionNoteAPI.as_view(),
        name='Transaction Notes'),

    url(r'transactions/commission/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionCommissionAPI.as_view(),
        name='Transaction Commission'),

    url(r'transactions/contract/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionContractAPI.as_view(),
        name='Transaction Contract'),

    url(r'transactions/document/$',
        TransactionDocumentAPI.as_view(),
        name='Transaction Documents'),



    url(r'transactions/document/(?P<document_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionDocumentAPI.as_view(),
        name='Transaction Documents'),



    url(r'transactions/secondary/(?P<tr_id>[a-zA-Z0-9.@_-]+)/$',
        TransactionSecondaryAPI.as_view(),
        name='Transaction Secondary'),

    url(r'transactions/(?P<tr_id>[a-zA-Z0-9.@_-]+)/status/$',
        TransactionBasicAPI.as_view(),
        name='Transaction Status'),

    # url(r'transactions/(?P<tr_id>[a-zA-Z0-9.@_-]+)/shipment/$',
    #     TransactionShipmentAPI.as_view(),
    #     name='Transaction Shipment'),

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

    url(r'pricing/product_item/(?P<product_item_price_id>[0-9]+)/$',
        ProductItemPricingAPI.as_view(),
        name='Product_Item_Pricing_API'),

    url(r'pricing/summary/$',
        PricingSummaryAPI.as_view(),
        name='Price_Summary_API'),

    # Product Pricing API

    url(r'^website/pricing/graph/(?P<product_item_id>[0-9]+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        WebsitePricingGraphAPI.as_view(),
        name='Website_Pricing_API'
        ),

    # Shipping API

    url('shipping/port_tag/$',
        ShippingPortTagAPI.as_view(),
        name='Shipping Ports List API'),

    url('shipping/vessel_tag/$',
        VesselTagAPI.as_view(),
        name='Shipping Ports List API'),


    url('shipping/vessel/list/$',
        VesselListAPI.as_view(),
        name='Shipping Ports List API'),

    url('shipping/vessel/$',
        VesselAPI.as_view(),
        name='Shipping Ports API'),

    url('shipping/vessel/(?P<vessel_id>[0-9]+)/$',
        VesselAPI.as_view(),
        name='Shipping Ports API'),


    url('shipping/line/list/$',
        ShippingLineListAPI.as_view(),
        name='Shipping Ports List API'),

    url('shipping/line/$',
        ShippingLineAPI.as_view(),
        name='Shipping Ports API'),

    url('shipping/line/(?P<line_id>[0-9]+)/$',
        ShippingLineAPI.as_view(),
        name='Shipping Ports API'),

    url('shipping/ports/list/$',
        ShippingPortListAPI.as_view(),
        name='Shipping Ports List API'),

    url('shipping/ports/$',
        ShippingPortAPI.as_view(),
        name='Shipping Ports API'),

    url('shipping/ports/(?P<port_id>[0-9]+)/$',
        ShippingPortAPI.as_view(),
        name='Shipping Ports API'),

    # Product Keyword API

    url(r'product/category/$',
        ProductsCategoryAPI.as_view(),
        name='Product_Category_API'),

    url(r'product/category/specification/$',
        ProductSpecificationAPI.as_view(),
        name='Product Specification API'),

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

    # Product Related API

    url(r'product/$',
        ProductsAPI.as_view(),
        name='Products'),

    url(r'product/product_tags/$',
        ProductTagsAPI.as_view(),
        name='Product_Tags'),

    url(r'product/website_status/$',
        ProductOnWebsiteAPI.as_view(),
        name='Products_Website_Status'),

    url(r'product/(?P<product_id>[0-9]+)/$',
        ProductsAPI.as_view(),
        name='Products'),

    url(r'product/origin/$',
        ProducOriginAPI.as_view(),
        name='Products Origins'),

    url(r'^product_item/$',
        ProductItemAPI.as_view(),
        name='Products_Item_API'),

    url(r'^product_item/specs/$',
        ProductItemSpecificationAPI.as_view(),
        name='Product_Specification_API'
        ),

    url(r'^product_item/price_on_website/$',
        ProductItemPriceOnWebsiteAPI.as_view(),
        name='Product_Item_Price_On_Website'),

    url(r'^product_item/price_report/$',
        ProductItemPriceReportAPI.as_view(),
        name='Product_Item_Price_Report'),

    # DropDownRelatedAPI
    url(r'^dropDown/',
        include('doniApi.dropDown.urls')),

    # Website Related APIs
    url(r'^contact_us/$',  ContactUsAPI.as_view(), {"public_api": True}, name='website-contact-us', ),

    url(r'^newsletter/$', NewsLetterAPI.as_view(), name='website-newsletter'),

    # Manifest Related API

    url(r'^manifest/$',
        ManifestAPI.as_view(),
        name='manifest_basic'),

    url(r'^manifest/(?P<manifest_id>[0-9]+)/$',
        ManifestAPI.as_view(),
        name='manifest_basic'),

    url(r'^manifest/dashboard/$',
        ManifestDashboardAPI.as_view(),
        name='manifest_dashboard'),


    # Currency Exchange

    url(r'^currency_exchange/dashboard/$',
        CurrencyExchangeDashboardAPI.as_view(),
        name='currency_dashboard'),

    # Accounts

    url(r'^accounts/invoice/$',
        InvoiceAPI.as_view(),
        name='Invoice API'),

    url(r'^accounts/commission_flow/$',
        CommissionFlowAPI.as_view(),
        name='Invoice API')


)
