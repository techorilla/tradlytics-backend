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

            from doniServer.routines import PriceSummaryRoutine
            obj = PriceSummaryRoutine()
            obj.run_routine()

        except Exception, e:

            log.exception("Exception in Price Summary Routine" % e)
            mail_admins(
                "Exception in Price Summary Routine",
                "Exception:%s\nTraceback:%s" % (
                    e, traceback.format_exc()))
