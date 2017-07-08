
from django.db import models
from datetime import datetime as dt


class CurrencyExchange(models.Model):
    currency_code_in = models.CharField(max_length=3, null=False)
    currency_code_out = models.CharField(max_length=3, null=False)
    exchange_rate = models.FloatField(null=False)
    exchange_rate_on = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = 'currency_exchange'
        ordering = ["-exchange_rate_on"]

    def get_graph_obj(self):
        return {
            'date': self.exchange_rate_on,
            'value': self.exchange_rate
        }

    def __unicode__(self):
        return '%s:%s:%s:%s' % (str(self.exchange_rate_on), self.exchange_rate,
                                self.currency_code_in, self.currency_code_out)

    @classmethod
    def already_exist(cls, date, input_currency, output_currency):
        cur = cls.objects.filter(exchange_rate_on=date, currency_code_in=input_currency,
                                 currency_code_out=output_currency)
        return cur.exists()

    @classmethod
    def save_exchange_rate(cls, rate, rate_on=None, input_currency='USD', output_Currency='PKR'):
        if rate_on is None:
            rate_on = dt.now().date()
        cur_exchange = CurrencyExchange()
        cur_exchange.currency_code_in = input_currency
        cur_exchange.currency_code_out = output_Currency
        cur_exchange.exchange_rate = rate
        cur_exchange.exchange_rate_on = rate_on
        cur_exchange.save()
