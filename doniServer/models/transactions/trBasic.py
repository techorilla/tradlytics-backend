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
from notifications.signals import notify
from functools import reduce
from django.db.models import Q, F
import operator
from datetime import datetime as dt
import pycountry
import re


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

    def delete(self):
        super(Transaction, self).save()


    @classmethod
    def get_business_type_drop_down_for_transaction_page(cls, business_type, business_id):
        def country_flag(business):
            # business['countryFlag'] = None if not business['country'] else 'flags/1x1/%s.svg' % business['country'].lower()
            if business['country']:
                try:
                    business['country'] = pycountry.countries.get(alpha_2=business['country']).common_name
                except AttributeError:
                    business['country'] = pycountry.countries.get(alpha_2=business['country']).name


        business_type = business_type.lower()
        location_query = [
            (business_type+'__locations__is_primary', True),
            (business_type + '__locations__isnull', True)
        ]
        location_query_list = [Q(query) for query in location_query]
        contact_person_query = [
            (business_type + '__contact_persons__is_primary', True),
            (business_type + '__contact_persons__isnull', True)
        ]
        contact_person_list = [Q(query) for query in contact_person_query]

        business_list = cls.objects.filter(created_by__profile__business_id=business_id) \
            .filter(reduce(operator.or_, location_query_list))\
            .filter(reduce(operator.or_, contact_person_list)).distinct()\
            .annotate(id=F(business_type+'__bp_id')).annotate(name=F(business_type+'__bp_name'))\
            .annotate(country=F(business_type+'__locations__country_name'))\
            .annotate(contactPerson=F(business_type+'__contact_persons__full_name'))\
            .values('id', 'name', 'country', 'contactPerson')\
            .order_by('name')
        # map(country_flag, business_list)
        return business_list

    @classmethod
    def get_self_contract_trades(cls, business):
        all_company_ids = business.app_profile.all_associated_companies_id
        return Transaction.objects.filter(created_by__profile__business=business) \
            .filter(contractual_buyer__bp_id__in=all_company_ids)

    @classmethod
    def get_trades_in_date_range(cls, business,start, end):
        return cls.objects.filter(created_by__profile__business=business)\
            .filter(date__lte=end).filter(date__gte=start)

    @classmethod
    def get_buyer_contract_trades_in_date_range(cls, business, start, end):
        all_company_ids = business.app_profile.all_associated_companies_id
        return Transaction.objects.filter(created_by__profile__business=business) \
            .exclude(contractual_buyer__bp_id__in=all_company_ids).filter(date__lte=end).filter(date__gte=start)

    @classmethod
    def get_all_business_completed_trades_in_date_range(cls, business, start, end):
        return Transaction.objects.filter(created_by__profile__business=business) \
            .filter(completion_status__is_complete=True) \
            .filter(completion_status__completion_date__lte=end).filter(completion_status__completion_date__gte=start)

    @classmethod
    def get_all_washout_trades_in_date_range(cls, business, start, end):
        return Transaction.objects.filter(created_by__profile__business=business) \
            .filter(washout__is_washout=True) \
            .filter(washout__washout_date__lte=end).filter(washout__washout_date__gte=start)

    @classmethod
    def get_arrived_at_port_not_completed_in_date_range(cls, business, start, end):
        return cls.objects.filter(created_by__profile__business=business) \
            .filter(Q(completion_status=None) | Q(completion_status__is_complete=False)) \
            .filter(shipment__arrived_at_port=True).filter(shipment__date_arrived__lte=end).filter(shipment__date_arrived__gte=start)

    @classmethod
    def get_all_business_completed_trades(cls, business):
        return Transaction.objects.filter(created_by__profile__business=business) \
            .filter(completion_status__is_complete=True)

    @classmethod
    def get_business_all_washout(cls, business):
        return Transaction.objects.filter(created_by__profile__business=business) \
            .filter(washout__is_washout=True)

    @classmethod
    def get_not_shipped_not_washout_not_completed(cls, business):
        return cls.objects.filter(created_by__profile__business=business) \
            .filter(Q(completion_status=None) | Q(completion_status__is_complete=False)) \
            .filter(Q(washout=None) | Q(washout__is_washout=False)) \
            .filter(shipment__not_shipped=True)\
            .filter(shipment_end__lt=dt.today())

    @classmethod
    def get_arrived_at_port_not_completed(cls, business):
        return cls.objects.filter(created_by__profile__business=business)\
            .filter(Q(completion_status=None)|Q(completion_status__is_complete=False)) \
            .filter(shipment__arrived_at_port=True)

    @classmethod
    def get_expected_arrival(cls, business):
        return cls.objects.filter(created_by__profile__business=business) \
                .filter(Q(completion_status=None) | Q(completion_status__is_complete=False)) \
                .filter(shipment__shipped=True)\
                .filter(shipment__arrived_at_port=False)






    def get_obj(self):
        partial_shipment = None if not hasattr(self, 'partial_shipment') \
            else self.partial_shipment.primary_shipment.file_id
        primary_trade = None if not hasattr(self, 'secondary_trade')\
            else self.secondary_trade.primary_trade.file_id

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
                'quantityFcl': str(round(self.quantity_fcl, 2)),
                'primaryShipment': partial_shipment,
                'primaryTransaction': primary_trade
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
        currency = business.app_profile.currency
        #Transaction change logs
        change_logs = self.change_log.all()
        change_logs = [log.get_obj() for log in change_logs]

        # Transaction Notes
        notes = self.notes.all().order_by('-created_at')
        notes = [note.get_obj(base_url, user) for note in notes]

        # Transaction Files
        files = self.files.values('file_name', 'extension', 'created_at', 'created_by__username', 'file_id') \
            .order_by('-created_at')

        #Invoice

        invoice = None if not self.invoices.exists() else self.invoices.all()[0]

        files = [{
                     'fileId': f.get('file_id'),
                     'fileName': f.get('file_name'),
                     'uploadedBy': f.get('created_by__username'),
                     'uploadedAt': f.get('created_at'),
                     'extension': f.get('extension'),
                 } for f in files]

        return {
            'id': self.tr_id,
            'onOurContract': business.app_profile.on_our_contract(self.contractual_buyer),
            'invoiceCreation': business.app_profile.on_our_contract(self.contractual_buyer) and not self.invoices.exists(),
            'businessCurrency': currency,
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
                'shipmentStart': self.shipment_start,
                'otherInfo': self.other_info
            },
            'invoice': None if not invoice else invoice.get_description_obj(),
            'completeObj': None if not hasattr(self, 'completion_status') else self.completion_status.get_description_obj(),
            'washOut': None if not hasattr(self, 'washout') else self.washout.get_description_obj(),
            'changeLogs': change_logs,
            'shipment': None if not hasattr(self, 'shipment') else self.shipment.get_description_object(base_url),
            'commission': self.commission.get_description_obj(base_url),
            'files': files,
            'notes': notes
        }

    class Meta:
        db_table = 'tr_basic'


from django.db.models.signals import post_save
from notifications.signals import notify

def my_handler(sender, instance, created, **kwargs):
    if created or not instance.updated_by:
        user = instance.created_by
        peers = user.profile.get_notification_peers()
        peer_notification = 'New International transaction with File Id <strong>%s</strong> created by %s'
        peer_notification = peer_notification%(instance.file_id, instance.created_by.username)
        notify.send(user, recipient=peers, verb=peer_notification, description='international_trade', state='dashboard.transactionView',
                    state_params={'id': instance.file_id}, user_image=user.profile.get_profile_pic())
    else:
        user = instance.updated_by
        peers = user.profile.get_notification_peers()
        peer_notification = 'International Transaction with File Id <strong>%s</strong> updated by %s'
        peer_notification = peer_notification % (instance.file_id, instance.created_by.username)
        notify.send(user, recipient=peers, verb=peer_notification, description='international_trade', state='dashboard.transactionView',
                    state_params={'id': instance.file_id}, user_image=user.profile.get_profile_pic())

post_save.connect(my_handler, sender=Transaction)



class SecondaryTrades(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        null=True,
        related_name='secondary_trade'
    )
    primary_trade = models.ForeignKey(Transaction, null=False, related_name='primary_trade')

    class Meta:
        db_table = 'transaction_secondary_trades'

class PartialShipments(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        null=True,
        related_name='partial_shipment'
    )
    primary_trade = models.ForeignKey(Transaction, null=False, related_name='primary_shipment')

    class Meta:
        db_table = 'transaction_partial_shipment'




