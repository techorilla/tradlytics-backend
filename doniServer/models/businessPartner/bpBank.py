from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .bpBasic import BpBasic
from cities_light.models import City


class BpBank(models.Model):
    bp = models.ForeignKey(BpBasic, null=False, blank=False, related_name='banks')
    acc_id = models.AutoField(primary_key=True)
    branch_address = models.CharField(max_length=250, null=False, blank=False)
    bank_name = models.CharField(max_length=100, null=False)
    acc_title = models.CharField(max_length=150, null=False)
    acc_number = models.CharField(max_length=100, null=False)
    acc_city = models.CharField(max_length=200, null=True)
    acc_country = models.CharField(max_length=250, null=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None,  null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_bank_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='bp_bank_updated_by')

    class Meta:
        db_table = 'bp_bank'

    def get_obj(self):
        city_options = dict()
        cities = City.objects.filter(country__code2=self.acc_country).filter().order_by('name_ascii')
        city_options['list'] = [
            {
                'id': city.name_ascii,
                'name': city.name_ascii
            } for city in cities]
        return {
            'id': self.acc_id,
            'accountTitle': self.acc_title,
            'accountNumber': self.acc_number,
            'accountCountry': self.acc_country,
            'accountCity': self.acc_city,
            'accountAddress': self.branch_address,
            'bankName': self.bank_name,
            'cityOptions': city_options
        }
