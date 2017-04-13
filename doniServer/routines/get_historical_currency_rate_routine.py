from doniScrapper.currencyScraper import CurrencyScrapper
from datetime import datetime as dt


class GetHistoricalCurrencyRateRoutine(object):

    def __init__(self):
        return None

    ## This routine is expected to run once

    def run_routine(self, start_date, input_currency, output_currency):
        cs = CurrencyScrapper()
        cs.get_currency_rate_from_date(start_date, input_currency, output_currency)


