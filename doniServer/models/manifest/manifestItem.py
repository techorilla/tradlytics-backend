from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ..businessPartner.bpBasic import BpBasic
from doniServer.models import BpLocation
from ..product import Products, PriceMetric
from django.db import connection
from django.contrib import admin
from django.db.models import Prefetch
from django.db.models import F
import pytz


class ManifestItem(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now, null=False)
    buyer = models.ForeignKey(BpBasic, null=False, related_name='buyer')
    seller = models.ForeignKey(BpBasic, null=False, related_name='seller')
    product = models.ForeignKey(Products, null=False, related_name='product_manifest')
    quantity = models.IntegerField(default=0)
    quantity_metric = models.ForeignKey(PriceMetric, null=False, related_name='manifest_metric')
    comments = models.TextField(null=True)
    container_no = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='manifest_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='manifest_updated_by')

    class Meta:
        db_table = 'manifest_item'
        ordering = ('-date',)

    @classmethod
    def get_manifest_items(cls, start_time, end_time):
        cur = connection.cursor()
        start_time = start_time.astimezone(pytz.utc).strftime("%Y-%m-%d 00:00:00")
        end_time = end_time.astimezone(pytz.utc).strftime("%Y-%m-%d 23:59:59")
        cur.callproc('manifest_item_list', [start_time, end_time, ])
        field_names = [i[0] for i in cur.description]
        manifest_items = cur.fetchall()
        cur.close()
        return [dict(zip(field_names, item)) for item in manifest_items]

    def get_list_obj(self):
        seller_country, seller_country_code, seller_country_flag = self.seller.primary_origin
        buyer_country, buyer_country_code, buyer_country_flag = self.buyer.primary_origin

        return {
            'id': self.id,
            'date': self.date,
            'buyerName': self.buyer.bp_name,
            'buyerId': self.buyer.bp_id,
            'buyerCountry': buyer_country,
            'buyerCountryFlag': buyer_country_flag,
            'buyerPrimaryContact': self.buyer.primary_contact,
            'sellerCountryFlag': seller_country_flag,
            'sellerName': self.seller.bp_name,
            'sellerCountry': seller_country,
            'sellerId': self.seller.bp_id,
            'sellerPrimaryContact': self.seller.primary_contact,
            'productId': self.product.id,
            'productName': self.product.name,
            'quantity': self.quantity,
            'quantityMetric': self.quantity_metric.metric if self.quantity_metric else None,
            'quantityMetricId': self.quantity_metric.metric if self.quantity_metric else None,
            'containerNo': self.container_no,
            'updatedBy': self.updated_by.username if self.updated_by else None,
            'updatedAt': self.updated_at,
            'createdBy': self.created_by.username if self.created_by else None,
            'createdAt': self.created_at
        }

    def get_obj(self):

        return {
            'id': self.id,
            'date': self.date,
            'buyerId': self.buyer.bp_id,
            'sellerId': self.seller.bp_id,
            'productId': self.product.id,
            'quantity': self.quantity,
            'containerNo': self.container_no,
            'quantityMetricId': self.quantity_metric.id if self.quantity_metric else None,
            'updatedBy': self.updated_by.username if self.updated_by else None,
            'updatedAt': self.updated_at,
            'createdBy': self.created_by.username if self.created_by else None,
            'createdAt': self.created_at
        }


