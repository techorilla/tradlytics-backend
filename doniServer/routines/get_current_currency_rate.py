from doniScrapper.currencyScraper import CurrencyScrapper
from doniServer.models import CurrencyExchange
from datetime import datetime as dt


class GetCurrentCurrencyRateRoutine(object):

    def __init__(self):
        return None

    # This routine is expected to run everyday at 12

    def run_routine(self, input_currency, output_currency):
        cs = CurrencyScrapper()
        today = dt.now().date()
        if not CurrencyExchange.already_exist(today, input_currency, output_currency):
            rate, date = cs.get_currency_rate(input_currency, output_currency)
            if rate and rate != 0.0:
                CurrencyExchange.save_exchange_rate(rate, rate_on=today,
                                                    input_currency=input_currency,
                                                    output_Currency=output_currency)







