from django.core.management import BaseCommand
import traceback
from django.core.mail import mail_admins
from doniCore.utils import log
from datetime import datetime as dt


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('input_currency', type=str)
        parser.add_argument('output_currency', type=str)


    def handle(self, *args, **options):

        input_currency = options['input_currency']
        output_currency = options['output_currency']

        """
        The command to fetch historical currency rates
        """

        help = "Fetch current day currency rates given a input currency code and output currency code"

        try:

            from doniServer.routines import GetCurrentCurrencyRateRoutine
            obj = GetCurrentCurrencyRateRoutine()
            obj.run_routine(input_currency, output_currency)

        except Exception, e:

            log.exception("Exception in get_current_rate_from_date: %s" % str(e))
            mail_admins(
                "Exception in Get Current Rate From Date",
                "Exception:%s\nTraceback:%s" % (
                    e, traceback.format_exc()))
