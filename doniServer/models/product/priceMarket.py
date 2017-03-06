from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin

import pycountry

def get_all_countries():
    all_countries = list(pycountry.countries)
    return [(country.alpha_2, country.name) for country in all_countries]


def get_all_currencies():
    all_currencies = list(pycountry.currencies)
    return [(currency.alpha_3, currency.name) for currency in all_currencies]


class PriceMarket(models.Model):
    id = models.AutoField(primary_key=True)
    origin = models.CharField(max_length=256, choices=[('INT', 'International')] + list(get_all_countries()))
    currency = models.CharField(max_length=20, choices=list(get_all_currencies()))
    description = models.TextField(null=True, default=None)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='price_market_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='price_market_updated_by')

    def get_dropdown(self):
        return {
            'id': self.id,
            'origin': self.country_name,
            'currency': self.currency
        }

    @property
    def country_name(self):
        if self.origin != 'INT':
            country = pycountry.countries.get(alpha_2=str(self.origin).upper())
            return country.name
        else:
            return 'International'

    def get_obj(self):
        return {
            'id': self.id,
            'countryName': self.country_name,
            'country': self.origin.upper() if self.origin != 'INT' else None,
            'currency': self.currency,
            'description': self.description,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
            'updated_by': self.updated_by.username if self.updated_by else None,
            'created_by': self.created_by.username,
            'isInternational': True if self.origin == 'INT' else False
        }

    class Meta:
        db_table = 'price_market'
        unique_together = ('origin', 'currency',)

    def __unicode__(self):
        return self.origin



from django.contrib import admin
from django_countries.widgets import CountrySelectWidget


class PriceMarketAdmin(admin.ModelAdmin):
    model = PriceMarket
    list_display = ('origin', 'currency', 'created_by', 'created_at')
    fieldsets = [
        ('Price Market', {'fields': ['origin', 'currency', 'description']}),
    ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()
