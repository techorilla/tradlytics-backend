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

            from doniScrapper.containerVessel import *
            get_vessel_position_for_all_business_app_profile()

        except Exception, e:

            log.exception("Exception in Transaction Shipment Tracking Routine" % e)
            mail_admins(
                "Exception in Transaction Shipment Tracking Routine",
                "Exception:%s\nTraceback:%s" % (
                    e, traceback.format_exc()))
