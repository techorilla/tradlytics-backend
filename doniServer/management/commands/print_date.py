from django.core.management import BaseCommand
import traceback
from django.core.mail import mail_admins
from doniCore.utils import log
from datetime import datetime as dt


class Command(BaseCommand):
    def handle(self, *args, **options):

        """
        The command to check if celery is up
        """
        date = dt.now().date()
        print str(date)