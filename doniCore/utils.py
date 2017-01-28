import logging
import os, sys
from django.conf import settings
from doniServer.models.authentication.userProfile import UserProfile

log = logging.getLogger("django")




class Utilities(object):
    @classmethod
    def get_user_business(cls, user):
        profile = UserProfile.objects.get(user=user)
        return profile.business

    @staticmethod
    def get_media_directory():
        return '/'.join(os.path.join(settings.BASE_DIR).split('/')[:-1])+'/media'
