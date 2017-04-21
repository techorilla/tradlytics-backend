from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from doniCore import log
from django.db import models


class UserSession(models.Model):
    user = models.ForeignKey(User, unique=True)
    last_session_key = models.CharField(
        blank=True, null=True, max_length=40)

    class Meta:
        db_table = 'user_sessions'

    @staticmethod
    def set_session_key(user, key):
        try:
            user_session, created = UserSession.objects.get_or_create(user=user)
            if user_session.last_session_key and user_session.last_session_key != key:
                try:
                    Session.objects.get(session_key=user_session.last_session_key).delete()
                except Session.DoesNotExist:
                    pass

            user_session.last_session_key = key
            user_session.save()
        except Exception, e:
            log.exception("Exception %s." % e)
