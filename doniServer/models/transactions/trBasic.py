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
    quantity_fcl = models.FloatField(default=0.00)
    quantity = models.FloatField(default=None)
    price = models.FloatField(default=None)
    packaging = models.ForeignKey(Packaging, null=True)
    shipment_start = models.DateField()
    shipment_end = models.DateField()
    is_complete = models.BooleanField(default=False)
    file_id = models.CharField(max_length=100, null=False, unique=True, blank=False)
    contract_id = models.CharField(max_length=100, null=True)
    other_info = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_basic_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_basic_updated_by')

    @property
    def get_washout_string(self):
        if not self.is_washout:
            return 'Washout Status Deactivated'
        if self.is_washout and (self.is_washout_at == self.price):
            return 'Washout At Par'
        if self.is_washout and (self.is_washout_at != self.price):
            return 'Washout At Price <span class="titled">USD %.2f</span>'%self.is_washout_at


    def get_obj(self):

        return {
            'id': self.tr_id,
            'commission': None,
            'productSpecification': self.product_specification,
            'basic': {
                'date': self.date,
                'buyerId': self.buyer.bp_id,
                'sellerId': self.seller.bp_id,
                'productItemId': self.product_item.id,
                'packagingId': self.packaging.id,
                'shipmentStart': self.shipment_start,
                'shipmentEnd': self.shipment_end,
                'contractualBuyerId': self.contractual_buyer.bp_id,
                'otherInfo': self.other_info,
                'fileId': self.file_id,
                'contractId': self.contract_id,
                'price': str(round(self.price,2)),
                'quantity': str(round(self.quantity,2)),
                'quantityFcl': str(round(self.quantity_fcl, 2))
            },
            'commission':{
                'sellerBrokerId': None if not self.commission.seller_broker else self.commission.seller_broker.bp_id,
                'buyerBrokerId': None if not self.commission.buyer_broker else self.commission.buyer_broker.bp_id,
                'buyerBrokerCommissionTypeId': None if not self.commission.buyer_broker_comm else  self.commission.buyer_broker_comm_type.id,
                'buyerBrokerCommission': str(round(self.commission.buyer_broker_comm,2)),
                'typeId': self.commission.commission_type.id,
                'discount': str(round(self.commission.discount,2)),
                'difference': str(round(self.commission.difference,2)),
                'commission': str(round(self.commission.commission,2))
            }
        }



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
            'expectedCommission':  self.commission.expected_commission,
            'actualCommission': self.commission.actual_commission
        }

    def get_complete_obj(self, base_url, user):

        business = user.profile.business
        #Transaction change logs
        change_logs = self.change_log.all()
        change_logs = [log.get_obj() for log in change_logs]

        # Transaction Notes
        notes = self.notes.all().order_by('-created_at')
        notes = [note.get_obj(base_url, user) for note in notes]

        # Transaction Files
        files = self.files.values('file_name', 'extension', 'created_at', 'created_by__username', 'file_id') \
            .order_by('-created_at')

        # Washout Detail

        washout_obj = {
            # 'status': self.is_washout,
            # 'washOutStr': self.get_washout_string,
            # 'isWashOutAt': '%.2f'%round(self.is_washout_at,2)
        }

        files = [{
                     'fileId': f.get('file_id'),
                     'fileName': f.get('file_name'),
                     'uploadedBy': f.get('created_by__username'),
                     'uploadedAt': f.get('created_at'),
                     'extension': f.get('extension'),
                 } for f in files]

        return {
                'id': self.tr_id,
                'isComplete': self.is_complete,
                'invoiceCreation': (self.contractual_buyer == business),
                'basic': {
                    'price': self.price,
                    'date': self.date,
                    'buyer':self.buyer.get_description_obj(base_url),
                    'seller': self.seller.get_description_obj(base_url),
                    'contractualBuyer': self.contractual_buyer.get_description_obj(base_url),
                    'productItem':  self.product_item.get_description_obj(base_url),
                    'contractNo': self.contract_id,
                    'fileNo': self.file_id,
                    'shipmentEnd': self.shipment_end,
                    'shipmentStart': self.shipment_start
                },
                'washOut': None if not hasattr(self, 'washout') else self.washout.get_description_obj(),
                'changeLogs': change_logs,
                'shipment': self.shipment.get_description_object(base_url),
                'commission': self.commission.get_description_obj(base_url),
                'files': files,
                'notes': notes
            }

    class Meta:
        db_table = 'tr_basic'
