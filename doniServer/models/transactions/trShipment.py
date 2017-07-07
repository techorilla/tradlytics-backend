from django.db import models
from datetime import date
from django.contrib.auth.models import User
from .trBasic import Transaction
from ..businessPartner import BpBasic
from ..shipment import ShippingPort

from django.utils import timezone


class TrShipment(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        null=True,
        related_name='shipment'
    )

    not_shipped = models.BooleanField(default=False)
    not_shipped_reason = models.TextField()
    extension = models.CharField(max_length=100)
    app_received = models.BooleanField(default=False)
    expected_shipment = models.DateField(default=None, null=True)
    in_transit = models.DateField(default=None, null=True)
    shipped = models.BooleanField(default=False)
    date_arrived = models.DateField(default=None, null=True)
    expected_arrival = models.DateField(default=None, null=True)
    transit_port = models.CharField(max_length=500, null=True)
    arrived_at_port = models.BooleanField(default=False)
    date_arrived = models.DateField(default=None, null=True)
    actual_arrived = models.DateField(default=None, null=True)
    bl_no = models.CharField(max_length=50, null=True)
    invoice_no = models.CharField(max_length=50, null=True)
    invoice_amount = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
    vessel_no = models.CharField(max_length=50)
    shipper_id = models.ForeignKey(BpBasic, null=True, related_name='tr_shipment_shipper')
    port_loading = models.ForeignKey(ShippingPort, null=True, related_name='tr_shipment_port_loading')
    port_destination = models.ForeignKey(ShippingPort, null=True, related_name='tr_shipment_port_destination')
    ship_line_details = models.TextField()
    chk_reason = models.BooleanField(default=False)
    chk_ship_ext = models.BooleanField(default=False)
    chk_exp_ship = models.BooleanField(default=False)
    chk_in_transit = models.BooleanField(default=False)
    chk_date_shipped = models.BooleanField(default=False)
    chk_expected_arrival = models.BooleanField(default=False)
    chk_transit_port = models.BooleanField(default=False)
    chk_date_arrived = models.BooleanField(default=False)
    chk_actual_arrived = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_shipment_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_shipment_updated_by')

    class Meta:
        db_table = 'tr_shipment'


    def get_description_object(self):

        return {
            'notShipped': {
                'active': self.not_shipped,
                'reason': self.not_shipped_reason,
                'shipmentExtension': self.extension

            },
            'approbationReceived':{
                'active': self.app_received,
                'expectedShipment': self.expected_shipment,
                'inTransit': self.in_transit,
            },
            'shipped':{
                'active': self.shipped
            },
            'arrivedAtPort':{
                'active': self.arrived_at_port,
                'quantityShipped': self.quantity,

            }
        }


