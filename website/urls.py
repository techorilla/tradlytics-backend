from django.conf.urls import url
from django.contrib import admin
from api.views import SingleBlog, ProductPage
from api.views import HomePage, BlogPage, SingleProductPage
from api.views import PricingPage, PricingDetail
from api.views import PrivacyPage
from django.views.generic.simple import direct_to_template


urlpatterns = [
    (r'^robots\.txt$', direct_to_template,
     {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    url(r'^$', HomePage.as_view(), name='homePage'),
    url(r'^research/$', BlogPage.as_view(), name='blogs'),
    url(r'^products/$', ProductPage.as_view(), name='products'),
    url(r'^product/$', SingleProductPage.as_view(), name='single_product'),
    url(r'^pricing/$', PricingPage.as_view(), name='pricingPage'),
    url(r'^research/(?P<slug>[\w-]+)/$', SingleBlog.as_view(), name='detail'),
    url(r'^price/analytics/$', PricingDetail.as_view(), name='pricing_detail'),
    url(r'^privacy/$', PrivacyPage.as_view(), name='privacy_policy')

]
