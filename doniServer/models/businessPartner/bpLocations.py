from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .bpBasic import BpBasic
from cities_light.models import City, Region
import pycountry
from django.conf import settings


class BpLocation(models.Model):
    bp = models.ForeignKey(BpBasic, null=False, blank=False, related_name='locations')
    address_id = models.AutoField(primary_key=True)
    address = models.TextField()
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    country_name = models.CharField(max_length=200, null=True)
    country_flag = models.CharField(max_length=100, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None,  null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_location_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='bp_location_updated_by')

    class Meta:
        db_table = 'bp_location'

    def save(self):
        country_name = pycountry.countries.get(alpha_2=self.country).name
        self.country_name = country_name
        self.country_flag = settings.COUNTRIES_FLAG_URL.replace('{code}', self.country.lower())
        super(BpLocation, self).save()

    @classmethod
    def re_save_all_business_location(cls):
        all_locations = cls.objects.all()
        for loc in all_locations:
            try:
                loc.save()
            except KeyError:
                pass

    def get_obj(self):
        regions = Region.objects.filter(country__code2=self.country).order_by('name')
        cityOptions = dict()
        stateOptions = dict()
        stateOptions['list'] = [{
                                    'id': state.name_ascii,
                                    'name': state.name_ascii
                                } for state in regions]

        if self.state:
            cities = City.objects.filter(country__code2=self.country).filter(region__name_ascii=self.state).order_by(
                'name_ascii')
        else:
            cities = City.objects.filter(country__code2=self.country).filter().order_by('name_ascii')

        cityOptions['list'] = [
            {
                'id': city.name_ascii,
                'name': city.name_ascii
            } for city in cities]
        return {
            'id': self.address_id,
            'address': self.address,
            'isPrimary': self.is_primary,
            'city': self.city,
            'cityOptions': cityOptions,
            'stateOptions': stateOptions,
            'state': self.state,
            'country': self.country,
            'created_by': self.created_by.username,
            'created_by_id': self.created_by.id,
            'created_at': self.created_at
        }

    @classmethod
    def drop_down_obj(cls, business):
        return cls.objects.extra(select={'id': 'address_id'}).filter(bp=business)\
            .values('id', 'address', 'city', 'state', 'country')
