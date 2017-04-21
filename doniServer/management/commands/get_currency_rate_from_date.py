from django.core.management import BaseCommand
import traceback
from django.core.mail import mail_admins
from doniCore.utils import log
from datetime import datetime as dt


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('date', type=str)
        parser.add_argument('input_currency', type=str)
        parser.add_argument('output_currency', type=str)


    def handle(self, *args, **options):

        start_date = options['date']
        input_currency = options['input_currency']
        output_currency = options['output_currency']

        """
        The command to fetch historical currency rates
        """

        help = "Fetch historical currency rates given a start date, input currency code and output currency code"

        try:

            from doniServer.routines import GetHistoricalCurrencyRateRoutine
            obj = GetHistoricalCurrencyRateRoutine()
            obj.run_routine(start_date, input_currency, output_currency)

        except Exception, e:

            log.exception("Exception in get_currency_rate_from_date: %s" % str(e))
            mail_admins(
                "Exception in Get Currency Rate From Date",
                "Exception:%s\nTraceback:%s" % (
                    e, traceback.format_exc()))
