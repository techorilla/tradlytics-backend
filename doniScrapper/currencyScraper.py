from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import timedelta
import requests
from doniServer.models import CurrencyExchange


class CurrencyScrapper(object):
    URL = 'http://www.forex.pk/currency-inter.php?base=%s&curr=%s'
    HIST_URL = 'http://x-rates.com/historical/?from=%s&amount=1&date=%s'

    EXCHANGE_PAD = {
        'PKR': 0.26
    }

    def get_currency_rate(self, currency_code_input='USD', currency_code_output='PKR'):
        today = dt.now()
        search_string = 'From %s to %s'
        week_before = today - timedelta(days=7)
        search_string = search_string % (week_before.strftime('%a, %b %d %Y'), today.strftime('%a, %b %d %Y'))
        url = self.URL % (currency_code_output, currency_code_input)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        currency_tag = soup.find('span', id='RATESPAN')
        value = float(currency_tag.text)
        return (value, today.date()) if search_string in str(soup) else (None, None)

    def get_historical_rate(self, date, currency_code_input='USD', currency_code_output='PKR'):
        page = requests.get(self.HIST_URL % (currency_code_output, date))
        soup = BeautifulSoup(page.text, 'html.parser')
        href = '/graph/?from=%s&to=%s' % (currency_code_input, currency_code_output)
        currency_tag = soup.find('a', href=href)
        value = float(currency_tag.text)
        return value + float(self.EXCHANGE_PAD[currency_code_output])

    def get_currency_rate_from_date(self, start_date=None, currency_code_input='USD', currency_code_output='PKR'):
        if start_date is None:
            start_date = dt.now()
            start_date = start_date - timedelta(days=365)
        else:
            start_date = dt.strptime(start_date, '%Y-%m-%d')
        end_date = dt.now()
        while start_date < end_date:
            if not CurrencyExchange.already_exist(start_date, currency_code_input, currency_code_output):
                try:
                    rate = self.get_historical_rate(str(start_date.date()), currency_code_input=currency_code_input,
                                                    currency_code_output=currency_code_output)
                    CurrencyExchange.save_exchange_rate(rate, rate_on=start_date.date(),
                                                        input_currency=currency_code_input,
                                                        output_Currency=currency_code_output)
                except Exception, e:
                    pass
            start_date = start_date + timedelta(days=1)














