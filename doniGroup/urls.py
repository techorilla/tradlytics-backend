"""doniGroup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from doniApi.authentication.Login import LoginAPI
from doniApi.authentication.Logout import LogOutAPI
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  url(r"api/login/$", LoginAPI.as_view(), {"public_api": True}, name="login"),
                  url(r"api/logout/$", LogOutAPI.as_view(), name="logout"),
                  url(r'^admin/', admin.site.urls),
                  url(r'^api/', include('doniApi.urls')),
                  url(r'^grappelli/', include('grappelli.urls')),
                  url(r'^', include("website.urls", namespace='web')),
                  url(r'^markdownx/', include('markdownx.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
