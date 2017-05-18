from django.db import models
from django.contrib.auth.models import User
from ..businessPartner.bpBasic import BpBasic
from ..product import ProductItem
from ..origins import Origin
from ..product import ProductsSpecification
from django.utils import timezone
from ..product import ProductKeyword
from ..dropDowns import Packaging
from jsonfield import JSONField


class Transaction(models.Model):
    tr_id = models.AutoField(primary_key=True)
    date = models.DateField(null=False)
    buyer = models.ForeignKey(BpBasic, null=False, related_name='tr_basic_buyer')
    contractual_buyer = models.ForeignKey(BpBasic, null=True, related_name='tr_contractual_buyer')
    seller = models.ForeignKey(BpBasic, null=False, related_name='tr_basic_seller')
    product_item = models.ForeignKey(ProductItem, null=True)
    product_specification = JSONField(null=True)
    quantity = models.FloatField(default=None)
    price = models.FloatField(default=None)
    packaging = models.ForeignKey(Packaging, null=True)
    shipment_start = models.DateField()
    shipment_end = models.DateField()
    file_id = models.CharField(max_length=100, null=False, unique=True, blank=False)
    contract_id = models.CharField(max_length=100, null=True)
    other_info = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_basic_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_basic_updated_by')


    def get_list_object(self):
        seller_country, seller_country_code, seller_country_flag = self.seller.primary_origin
        buyer_country, buyer_country_code, buyer_country_flag = self.buyer.primary_origin
        return {
            'id': self.tr_id,
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
            'fileNo': self.file_id,
            'price': self.price,
            'productName': self.product_item.product_origin.product.name,
            'productItemId': self.product_item.id,
            'productOriginName': self.product_item.product_origin.country.name,
            'productOriginFlag': self.product_item.product_origin.country.flag,
            'quantity': self.quantity,
            'sellerPrimaryContact': self.seller.primary_contact,
            'shipmentEnd': self.shipment_end,
            'shipmentStart': self.shipment_start,
            'expectedCommission':  self.commission.net_commission
        }



    class Meta:
        db_table = 'tr_basic'
