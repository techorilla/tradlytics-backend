from __future__ import unicode_literals

from django.db import models
from doniServer.models import Transaction
from doniInventory.models import Warehouse
from doniServer.models import BpBasic, ProductItem
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
import dateutil.parser
from django.db.models import Q, F
import operator
from doniServer.fields import VarBinaryField



PAYMENT_TERMS = {
    'ADVANCE': 'advance',
    'PRODUCT_DELIVERY': 'product_delivery',
    'ON_DATE': 'on_date'
}

class LocalTrade(models.Model):
    date = models.DateField(null=False)
    local_buyer = models.ForeignKey(BpBasic, null=False, related_name='tr_local_buyer')
    local_seller = models.ForeignKey(BpBasic, null=False, related_name='tr_local_seller')
    product_item = models.ForeignKey(ProductItem, null=False, related_name ='tr_local_product')
    quantity_fcl = models.FloatField(default=0.00)
    quantity = models.FloatField(default=None)
    price = models.FloatField(default=None)
    file_id = models.CharField(max_length=100, null=False, blank=False)
    international_file = models.ForeignKey(Transaction, null=True)
    contract_id = models.CharField(max_length=100, null=True)
    other_info = models.TextField()
    business = models.ForeignKey(BpBasic, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_local_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_local_updated_by')


    def get_complete_obj(self, base_url, user):
        business = user.profile.business
        currency = business.app_profile.currency
        notes = []
        files = self.local_trade_files.values('file_name', 'extension', 'created_at', 'created_by__username', 'file_id') \
            .order_by('-created_at')

        international_file_id = self.associated_international_trade.all().values('transaction_associated__file_id')
        local_file_id = self.associated_local_trade.all().values('local_trade_associated__file_id')


        international_file_id = [trade.get('transaction_associated__file_id') for trade in international_file_id]
        local_file_id = [trade.get('local_trade_associated__file_id') for trade in local_file_id]


        return {
            'files': files,
            'price': self.price,
            'quantity': self.quantity,
            'quantityFCL': self.quantity_fcl,
            'date': self.date,
            'currency': currency,
            'buyerId': self.local_buyer.bp_id,
            'sellerId': self.local_seller.bp_id,
            'productItemId': self.product_item.id,
            'buyer':self.local_buyer.get_description_obj(base_url),
            'seller': self.local_seller.get_description_obj(base_url),
            'productItem':  self.product_item.get_description_obj(base_url),
            'contractId': self.contract_id,
            'fileId': self.file_id,
            'fundsDueDate': self.status.funds_due_date,
            'deliveryDueDate': self.status.delivery_due_date,
            'otherInfo': self.other_info,
            'internationalFileId': international_file_id,
            'localFileId': local_file_id,
            'paymentTerm': None if not hasattr(self, 'payment_term') else self.payment_term.payment_term_string
        }

    def get_obj(self):
        business = user.profile.business
        currency = business.app_profile.currency
        international_file_id = self.associated_international_trade.all().values('transaction_associated__file_id')
        local_file_id = self.associated_local_trade.all().values('local_trade_associated__file_id')

        international_file_id = [trade.get('transaction_associated__file_id') for trade in international_file_id]
        local_file_id = [trade.get('local_trade_associated__file_id') for trade in local_file_id]
        return {
            'price': self.price,
            'quantity': self.quantity,
            'quantityFCL': self.quantity_fcl,
            'date': self.date,
            'currency': currency,
            'buyerId': self.local_buyer.bp_id,
            'sellerId': self.local_seller.bp_id,
            'productItemId': self.product_item.id,
            'buyer': self.local_buyer.get_description_obj(base_url),
            'seller': self.local_seller.get_description_obj(base_url),
            'productItem': self.product_item.get_description_obj(base_url),
            'contractId': self.contract_id,
            'fileId': self.file_id,
            'fundsDueDate': self.status.funds_due_date,
            'deliveryDueDate': self.status.delivery_due_date,
            'otherInfo': self.other_info,
            'internationalFileId': international_file_id,
            'localFileId': local_file_id,
            'paymentTerm': None if not hasattr(self, 'payment_term') else self.payment_term.payment_term_string
        }

    class Meta:
        unique_together = ('file_id', 'business',)

    @classmethod
    def get_trades_in_date_range(cls, business, start=None, end=None):
        if start and end:
            return cls.objects.filter(business=business) \
                .filter(date__lte=end).filter(date__gte=start)
        else:
            return cls.objects.filter(business=business)

    @classmethod
    def get_business_type_drop_down_for_transaction_page(cls, business_type, business_id):
        print business_type
        business_type = business_type.lower()
        business_type = business_type.replace(' ', '_')
        location_query = [
            (business_type + '__locations__is_primary', True),
            (business_type + '__locations__isnull', True)
        ]
        location_query_list = [Q(query) for query in location_query]
        contact_person_query = [
            (business_type + '__contact_persons__is_primary', True),
            (business_type + '__contact_persons__isnull', True)
        ]
        contact_person_list = [Q(query) for query in contact_person_query]

        business_list = cls.objects.filter(created_by__profile__business_id=business_id) \
            .values(*[business_type]).distinct() \
            .filter(reduce(operator.or_, location_query_list)) \
            .filter(reduce(operator.or_, contact_person_list)) \
            .annotate(id=F(business_type + '__bp_id')).annotate(name=F(business_type + '__bp_name')) \
            .annotate(country=F(business_type + '__locations__country_name')) \
            .annotate(contactPerson=F(business_type + '__contact_persons__full_name')) \
            .values('id', 'name', 'country', 'contactPerson') \
            .order_by('name')
        # map(country_flag, business_list)
        return business_list

class AssociatedLocalTrade(models.Model):
    local_trade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='associated_local_trade'
    )
    local_trade_associated = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='associated_with_local'

    )

class AssociatedInternationalTrade(models.Model):
    local_trade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='associated_international_trade'
    )
    transaction_associated = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='associated_with_international'
    )

class LocalTradeChangeLog(models.Model):
    local_trade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        null=True,
        related_name='change_log'
    )
    time = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user = models.ForeignKey(User, null=False, blank=False, related_name='local_trade_changes_by')

    class Meta:
        db_table = 'local_change_log'

    def get_obj(self):
        return {
            'changeByUserName': self.user.username,
            'changeByUserId': self.user.id,
            'description': self.description,
            'changeTime': self.time
        }

    @classmethod
    def add_change_log(cls, user, description, local_trade):
        change_log = cls()
        change_log.user = user
        change_log.description = description
        change_log.local_trade = local_trade
        change_log.save()

class LocalTradeNotes(models.Model):
    localTrade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    note_id = models.AutoField(primary_key=True)
    note = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='local_note_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='local_note_updated_by')

    def get_obj(self, base_url, user):
        return {
            'self': (self.created_by == user),
            'noteId': self.note_id,
            'isDeleteAble': (self.created_by == user) or user.is_superuser,
            'note': self.note,
            'createdAt': self.created_at,
            'createdBy': self.created_by.username,
            'createdByPic': self.created_by.profile.get_profile_pic(base_url),
            'updatedAt': self.updated_by
        }

    class Meta:
        db_table = 'local_notes'

class LocalTradeStatus(models.Model):
    local_trade = models.OneToOneField(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='status'
    )
    delivery_due_date = models.DateField(null=True)
    delivery_done = models.BooleanField(default=False)
    delivery_done_date = models.DateField(null=True)
    delivery_reached = models.BooleanField(default=False)
    delivery_reached_date = models.DateField(null=True)
    funds_due = models.BooleanField(default=False)
    funds_due_date = models.DateField(null=True)
    completion_status = models.BooleanField(default=False)
    completion_status_date = models.DateField(null=True)
    actual_weight = models.FloatField(null=True)
    actual_amount = models.FloatField(null=True)


    @classmethod
    def save_delivery_due_date(cls, local_trade, delivery_due_date, funds_due_date):
        print local_trade, delivery_due_date
        status = LocalTradeStatus() if not hasattr(local_trade, 'status') else local_trade.status
        status.local_trade = local_trade
        if delivery_due_date:
            delivery_due_date = dateutil.parser.parse(str(delivery_due_date).replace('"', ''))
            delivery_due_date = delivery_due_date.replace(hour=0, minute=0, second=0, microsecond=0)
            status.delivery_due_date = str(delivery_due_date.date())
        if funds_due_date:
            funds_due_date = dateutil.parser.parse(str(funds_due_date).replace('"', ''))
            funds_due_date = funds_due_date.replace(hour=0, minute=0, second=0, microsecond=0)
            status.funds_due_date = str(funds_due_date.date())
        status.save()

PAYMENT_TERMS = {
    'ADVANCE': 'advance',
    'PRODUCT_DELIVERY': 'product_delivery',
    'ON_DATE': 'on_date'
}


class PaymentTerm(models.Model):
    local_trade = models.OneToOneField(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='payment_term'
    )
    advance = models.BooleanField(default=False)
    on_delivery_reached = models.BooleanField(default=False)
    on_date = models.BooleanField(default=False)
    on_date_date = models.DateField(null=True)

    @property
    def payment_term_string(self):
        if self.advance:
            return PAYMENT_TERMS['ADVANCE']
        elif self.on_delivery_reached:
            return PAYMENT_TERMS['PRODUCT_DELIVERY']
        elif self.on_date:
            return PAYMENT_TERMS['on_date']

    @classmethod
    def save_payment_term(cls, local_trade, term, on_date=None):
        payment_term = PaymentTerm() if not hasattr(local_trade, 'payment_term') else local_trade.payment_term
        payment_term.local_trade = local_trade
        if term == 'advance':
            payment_term.advance = True
        elif term == 'product_delivery':
            payment_term.on_delivery_reached = True
        elif term == 'on_date':
            payment_term.on_date = True
            if on_date:
                on_date = dateutil.parser.parse(str(on_date).replace('"', ''))
                on_date = on_date.replace(hour=0, minute=0, second=0, microsecond=0)
                payment_term.on_date_date = on_date
        payment_term.save()



    def save(self):
        if self.advance or self.on_delivery_reached:
            self.on_date_date = None
        super(PaymentTerm, self).save()

class DeliverySlip(models.Model):
    date = models.DateField(null=False)
    delivery_date = models.DateField(null=True)
    warehouse = models.ForeignKey(Warehouse, null=False)
    lot_no = models.CharField(max_length=10, null=False)
    localTrade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='delivery_slip'
    )
    notes = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='local_delivery_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='local_delivery_updated_by')

class LocalTradePayments(models.Model):
    payment_received = models.FloatField()
    payment_date = models.DateField(null=False)

    class Meta:
        db_table = 'local_tr_payments'

class LocalFiles(models.Model):
    local_trade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='local_trade_files'
    )
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=400, null=True)
    file = VarBinaryField()
    extension = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='local_file_created_by')

    class Meta:
        db_table = 'local_tr_files'
