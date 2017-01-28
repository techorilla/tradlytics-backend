from django.db import models
from django.contrib.auth.models import User
from ..businessPartner.bpBasic import BpBasic
from ..product import Products
from ..origins import Origin
from ..product import ProductsSpecification
from django.utils import timezone
from ..product import ProductKeyword


class Transaction(models.Model):
    tr_id = models.AutoField(primary_key=True)
    date = models.DateField(null=False)
    buyer = models.ForeignKey(BpBasic, null=False, related_name='tr_basic_buyer')
    seller = models.ForeignKey(BpBasic, null=False, related_name='tr_basic_seller')
    product = models.ForeignKey(Products, null=False)
    origin = models.ForeignKey(Origin, null=False)
    specification = models.OneToOneField(
        ProductsSpecification,
        null=True
    )
    quality = models.OneToOneField(
        ProductKeyword,
        null=True
    )
    quantity = models.FloatField(default=None)
    price = models.FloatField(default=None)
    packing = models.CharField(max_length=50)
    shipment_start = models.DateField()
    shipment_end = models.DateField()
    file_id = models.CharField(max_length=100, null=False, unique=True, blank=False)
    contract_id = models.CharField(max_length=100, null=True)
    other_info = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_basic_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_basic_updated_by')

    class Meta:
        db_table = 'tr_basic'
