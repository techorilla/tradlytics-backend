from oauth2client import client
from django.conf import settings
from django.db import models
from jsonfield import JSONCharField, JSONField
from doniServer.models import BpBasic


class GoogleAnalyticsToken(models.Model):

    business = models.ForeignKey(BpBasic)
    data = JSONCharField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)








