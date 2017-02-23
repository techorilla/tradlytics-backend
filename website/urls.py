from django.conf.urls import url
from django.contrib import admin
from api.views import SingleBlog, ProductPage
from api.views import HomePage, BlogPage, SingleProductPage

urlpatterns = [
    url(r'^$', HomePage.as_view(), name='homePage'),
    url(r'^blogs/$', BlogPage.as_view(), name='blogs'),
    url(r'^products/$', ProductPage.as_view(), name='products'),
    url(r'^product/$', SingleProductPage.as_view(), name='single_product'),
    url(r'^(?P<slug>[\w-]+)/$', SingleBlog.as_view(), name='detail'),
]
