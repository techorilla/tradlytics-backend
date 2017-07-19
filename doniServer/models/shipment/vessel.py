from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .shippingLine import ShippingLine

import os


def get_image_path(instance, filename):
    return os.path.join('vessels', str(instance.imo_number+'_'+filename))


class Vessel(models.Model):
    imo_number = models.CharField(max_length=20)
    mmsi_number = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=300, null=True)
    broken = models.BooleanField(default=False)
    first_name = models.CharField(max_length=300)
    nationality = models.CharField(max_length=200)
    owner = models.CharField(max_length=300)
    operator = models.CharField(max_length=300, null=True)
    completion_year = models.CharField(max_length=100)
    shipyard = models.CharField(max_length=300)
    hull_number = models.CharField(max_length=100, null=True)
    engine_design = models.CharField(max_length=100)
    engine_type = models.CharField(max_length=100)
    engine_power_output = models.CharField(max_length=100)
    max_speed = models.CharField(max_length=100)
    over_all_length_m = models.CharField(max_length=100)
    over_all_beam_m = models.CharField(max_length=100)
    max_draught_m = models.CharField(max_length=100)
    max_TEU_capacity = models.CharField(max_length=100)
    container_capacity_at_14t_teu = models.CharField(max_length=100)
    reefer_containers_TEU = models.CharField(max_length=100)
    dead_weight_ton = models.CharField(max_length=100)
    gross_tonnage_ton = models.CharField(max_length=100)
    handling_gear = models.CharField(max_length=100)



    shipping_line = models.ForeignKey(ShippingLine, null=True, related_name='vessels')

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='vessel_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='vessel_updated_by')

    def get_list_obj(self, base_url):
        return {
            'id': self.id,
            'imoNumber': self.imo_number,
            'broken': self.broken,
            'nationality': self.nationality,
            'operator': self.operator,
            'name': self.first_name,
            'shippingLine': None if not self.shipping_line else self.shipping_line.get_obj(base_url)
        }

    def get_complete_obj(self):

        return {
            'id': self.id,
            'imoNumber': self.imo_number,
            'mmsi': self.mmsi_number,
            'name': self.first_name,
            'shippingLineId': None if not self.shipping_line else self.shipping_line.id
        }

    def get_tag_obj(self):
        return {
            'first_name': self.first_name,
            'imo_number': self.imo_number,
            'id': self.id,
            'mmsi_number': self.mmsi_number
        }

    def get_drop_down_obj(self):
        return {
            'imoNumber': self.imo_number,
            'mmsi': self.mmsi_number,
            'name': self.first_name
        }