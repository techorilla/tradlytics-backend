
from django.core.management import BaseCommand
import traceback
from django.core.mail import mail_admins
from doniCore.utils import log


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        """
        The command to check if celery is up
        """

        try:
            
            from celery.task.control import inspect
            i = inspect()
            if not bool(i.ping()):
                log.info("No Celery Node responded")
                mail_admins(
                    "IMP: CELERY IS DOWN!!", 
                    "Please restart..")
            else:
                log.info("Celery is running")

        except Exception, e:

            log.exception("Exception while checking for celery%s" % e)
            mail_admins(
                "Exception in Celery Check",
                "Exception:%s\nTraceback:%s" % (
                    e, traceback.format_exc()))
