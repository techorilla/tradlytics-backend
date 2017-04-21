from oauth2client import client
from django.conf import settings
from django.db import models
from jsonfield import JSONCharField, JSONField
from doniServer.models import BpBasic
from django.contrib.auth.models import User


class GoogleAnalyticsToken(models.Model):
    business = models.ForeignKey(BpBasic, related_name='ga_token')
    data = JSONCharField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=False, related_name='ga_token_user')








