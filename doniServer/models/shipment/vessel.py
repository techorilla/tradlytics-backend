from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ..businessPartner.bpBasic import BpBasic
import os


def get_image_path(instance, filename):
    return os.path.join('vessels', str(instance.imo_number+'_'+filename))


class Vessel(models.Model):
    imo_number = models.CharField(max_length=20, unique=True)
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
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='vessel_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='vessel_updated_by')