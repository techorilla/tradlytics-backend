from django.core.management import BaseCommand
import traceback
from django.core.mail import mail_admins
from doniCore.utils import log
from doniETL.etlMySqlServer import get_files_for_all_trades


class Command(BaseCommand):
    def handle(self, *args, **options):

        """
        The command to check if celery is up
        """

        try:



            get_files_for_all_trades()


        except Exception, e:
            print 'Error'
            log.exception("Exception while getting files from old ERP %s" % e)
            mail_admins(
                "Exception in Celery Check",
                "Exception:%s\nTraceback:%s" % (
                    e, traceback.format_exc()))
