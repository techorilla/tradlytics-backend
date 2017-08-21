from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from doniServer.models import Products, BpBasic
from django.contrib.auth.models import User
from datetime import timedelta
from django.db.models import Sum, F
from django.db.models import CharField, Case, Value, When
from django.db.models import IntegerField

# Create your models here.


class Warehouse(models.Model):

    name = models.CharField(max_length=200)
    address = models.TextField()
    contact = models.TextField()
    go_down_contact = models.CharField(max_length=250)
    go_down_keeper = models.CharField(max_length=250)
    self_warehouse = models.BooleanField(default=False)
    total_capacity_kgs = models.FloatField(default=0.00)
    business = models.ForeignKey(BpBasic, null=True, related_name='business_warehouse_added', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='warehouse_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='warehouse_updated_by')

    class Meta:
        db_table = 'inventory_warehouse'

    def __unicode__(self):
        return self.name

    def drop_down_obj(self):
        return {
            'name': self.name,
            'id': self.id
        }

    def get_complete_obj(self, with_rent=False):
        complete_obj = {
            'id': self.id,
            'name': self.name,
            'selfWarehouse': self.self_warehouse,
            'totalCapacity': self.total_capacity_kgs,
            'consumedCapacity': 'NA',
            'address': self.address,
            'contact': self.contact,
            'rentPer50Kg': 'NA',
            'rentList': []
        }

        if with_rent:
            all_rent = self.warehouse_rent.all().order_by('-date_change')
            if len(all_rent):
                complete_obj['rentPer50Kg'] = all_rent[0].rent
            all_rent = [rent.get_list_obj() for rent in all_rent]
            complete_obj['rentList'] = all_rent

        return complete_obj

    def get_warehouse_list_obj(self):
        last_rent = self.warehouse_rent.all().order_by('-date_change').first()
        rent_per_50kg =  last_rent.rent if last_rent else 'NA'
        return {
            'id': self.id,
            'name': self.name,
            'selfWarehouse': self.self_warehouse,
            'totalCapacity': self.total_capacity_kgs,
            'consumedCapacity': self.get_current_weight_stored_in_kgs,
            'rentPer50Kg': rent_per_50kg
        }



    def dashboard_warehouse_card(self):
        capacity_consumed =  self.get_current_weight_stored_in_kgs
        total_capacity = self.total_capacity_kgs
        percentage_consumed = (capacity_consumed/total_capacity)*100
        return {
            'id':self.id,
            'currentKgs': capacity_consumed,
            'name': self.name,
            'totalCapacity': total_capacity,
            'percentageConsumed': percentage_consumed
        }

    @property
    def get_current_weight_stored_in_kgs(self):
        total_out_flow = self.record.filter(positive=False)\
            .aggregate(Sum('trucks__weight_in_kg')).get('trucks__weight_in_kg__sum', 0.00)

        total_in_flow = self.record.filter(positive=True) \
            .aggregate(Sum('trucks__weight_in_kg')).get('trucks__weight_in_kg__sum', 0.00)

        total_in_flow = total_in_flow if total_in_flow else 0.00
        total_out_flow = total_out_flow if total_out_flow else 0.00
        return total_in_flow - total_out_flow

    def get_product_report(self, all_self_business_id, product_id, product_name):
        total_out_flow = self.record.filter(positive=False).filter(product__id=product_id)\
            .aggregate(Sum('trucks__weight_in_kg')).get('trucks__weight_in_kg__sum', 0.00)
        total_in_flow = self.record.filter(positive=True).filter(product__id=product_id) \
            .aggregate(Sum('trucks__weight_in_kg')).get('trucks__weight_in_kg__sum', 0.00)
        total_in_flow = total_in_flow if total_in_flow else 0.00
        total_out_flow = total_out_flow if total_out_flow else 0.00
        quantity_in_stock = total_in_flow - total_out_flow

        total_self_out_flow = self.record.filter(positive=False)\
            .filter(transaction_business__bp_id__in=all_self_business_id).filter(product__id=product_id) \
            .aggregate(Sum('trucks__weight_in_kg')).get('trucks__weight_in_kg__sum', 0.00)
        total_self_out_flow = total_self_out_flow if total_self_out_flow else 0.00

        total_self_in_flow = self.record.filter(positive=True) \
            .filter(transaction_business__bp_id__in=all_self_business_id).filter(product__id=product_id) \
            .aggregate(Sum('trucks__weight_in_kg')).get('trucks__weight_in_kg__sum', 0.00)
        total_self_in_flow = total_self_in_flow if total_self_in_flow else 0.00

        self_quantity = total_self_in_flow-total_self_out_flow

        other_self_out_flow = self.record.filter(positive=False) \
            .exclude(transaction_business__bp_id__in=all_self_business_id).filter(product__id=product_id) \
            .aggregate(Sum('trucks__weight_in_kg')).get('trucks__weight_in_kg__sum', 0.00)
        other_self_out_flow = other_self_out_flow if other_self_out_flow else 0.00

        other_self_in_flow = self.record.filter(positive=True) \
            .exclude(transaction_business__bp_id__in=all_self_business_id).filter(product__id=product_id) \
            .aggregate(Sum('trucks__weight_in_kg')).get('trucks__weight_in_kg__sum', 0.00)
        other_self_in_flow = other_self_in_flow if other_self_in_flow else 0.00

        other_business_quantity = other_self_in_flow - other_self_out_flow

        stock_percentage = (quantity_in_stock/self.get_current_weight_stored_in_kgs)*100

        return {
            'stockPercentage': stock_percentage,
            'quantityInStock': quantity_in_stock,
            'productName': product_name,
            'selfQuantity': self_quantity,
            'otherBusinessQuantityInStock': other_business_quantity
        }

    def get_business_product_report(self, business_id, business_name):
        quantity_in_stock, business_in_flow, business_out_flow = self.get_business_quantity_details(business_id)
        product_flow = self.get_business_product_distribution(business_id, quantity_in_stock)
        return {
            'productFlow': product_flow,
            'business_name': business_name,
            'businessInFlow': business_in_flow,
            'businessOutFlow': business_out_flow,
            'quantityInStock': quantity_in_stock,
            'quantityPercentage': float(quantity_in_stock/self.get_current_weight_stored_in_kgs)*100
        }

    def get_business_product_distribution(self, business_id, quantity_in_stock=None):

        business_product_in_flow = self.record.filter(positive=True).filter(transaction_business__bp_id=business_id) \
            .values('product__id', 'product__name')\
            .annotate(Sum('trucks__weight_in_kg'))

        business_product_out_flow = self.record.filter(positive=False).filter(transaction_business__bp_id=business_id) \
            .values('product__id', 'product__name') \
            .annotate(Sum('trucks__weight_in_kg'))

        in_flow_for_out_flow_found = []

        def get_flow_objects(in_flow):
            out_flow = next((flow for flow in business_product_out_flow if flow['product__id'] == in_flow['product__id']), None)
            if out_flow:
                in_flow_for_out_flow_found.append(out_flow['product__id'])
            trucks_out_flow = 0.00 if not out_flow else out_flow.get('trucks__weight_in_kg__sum', 0.00)
            in_flow['truckOutFlow'] = trucks_out_flow
            in_flow['truckInFlow'] = in_flow.get('trucks__weight_in_kg__sum', 0.00)
            in_flow['currentQuantity'] = in_flow['truckInFlow'] - in_flow['truckOutFlow']
            if quantity_in_stock:
                in_flow['quantityPercentage'] = (in_flow['currentQuantity']/quantity_in_stock)*100
            return in_flow

        product_distribution = map(get_flow_objects, business_product_in_flow)

        out_flow_with_no_in_flow_found = [flow for flow in business_product_out_flow if flow['product__id'] not in in_flow_for_out_flow_found]

        def add_out_flow_with_no_inflow(out_flow):
            out_flow['truckOutFlow'] = 0.00 if not out_flow else out_flow.get('trucks__weight_in_kg__sum', 0.00)
            out_flow['truckInFlow'] = 0.00
            out_flow['currentQuantity'] = 0.00
            out_flow['quantityPercentage'] = 0.00
            product_distribution.append(out_flow)

        map(add_out_flow_with_no_inflow, out_flow_with_no_in_flow_found)
        return product_distribution

    def get_business_quantity_details(self, business_id):
        business_out_flow = self.record.filter(positive=False).filter(transaction_business__bp_id=business_id) \
            .aggregate(Sum('trucks__weight_in_kg')).get('trucks__weight_in_kg__sum', 0.00)
        business_in_flow = self.record.filter(positive=True).filter(transaction_business__bp_id=business_id) \
            .aggregate(Sum('trucks__weight_in_kg')).get('trucks__weight_in_kg__sum', 0.00)
        business_out_flow = business_out_flow if business_out_flow else 0.00
        business_in_flow = business_in_flow if business_in_flow else 0.00
        business_quantity_in_stock = business_in_flow - business_out_flow
        return business_quantity_in_stock, business_in_flow, business_out_flow

class WarehouseRent(models.Model):
    warehouse = models.ForeignKey(Warehouse, null=False, related_name='warehouse_rent')
    date_change = models.DateField(null=False)
    data_end = models.DateField(null=True)
    rent = models.FloatField(default=0.00)
    currency = models.CharField(max_length=5, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='warehouse_rent_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='warehouse_rent_updated_by')

    class Meta:
        db_table = 'inventory_warehouse_rent'

    def update_last_warehouse_rent(self):
        last_warehouse_rent = WarehouseRent.objects.filter(warehouse=self.warehouse).order_by('-date_change').first()
        if last_warehouse_rent:
            last_warehouse_rent.data_end = self.date_change - timedelta(days=1)
            last_warehouse_rent.save()

    @classmethod
    def get_last_warehouse_rent_date(cls, warehouse_id):
        last_warehouse_rent = cls.objects.filter(warehouse_id=warehouse_id).order_by('-date_change').first()
        if last_warehouse_rent:
            return last_warehouse_rent.date_change
        else:
            return None


    def save(self):
        currency = self.created_by.profile.business.app_profile.currency

        self.currency = currency
        super(WarehouseRent, self).save()

    def get_list_obj(self):
        return {
            'rent': self.rent,
            'dateChange': self.date_change,
            'dateEnd': self.data_end
        }




    def __unicode__(self):
        return '%s:%s:%s'%(self.warehouse.name, self.date_change, self.rent)

class InventoryTransaction(models.Model):
    warehouse = models.ForeignKey(Warehouse, null=False, related_name='record')
    lot_no = models.CharField(max_length=10, default='MIX')
    date = models.DateField(null=False)
    transaction_business = models.ForeignKey(BpBasic, null=True, on_delete=models.SET_NULL)
    port_clearing_no = models.CharField(max_length=50, null=True)
    fcl_quantity = models.IntegerField(default=0.00)
    product = models.ForeignKey(Products, null=False)
    positive = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='inventory_record_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='inventory_record_updated_by')

    class Meta:
        db_table = 'inventory_transaction'

    def get_complete_obj(self):
        all_trucks = self.trucks.all()
        trucks = [truck.get_obj() for truck in all_trucks]
        return {
            'id': self.id,
            'warehouseId': self.warehouse.id,
            'lotNo': self.lot_no,
            'date': self.date,
            'businessId': self.transaction_business.bp_id,
            'portClearingNo': self.port_clearing_no,
            'fclQuantity': self.fcl_quantity,
            'productId': self.product.id,
            'positive': self.positive,
            'trucks':trucks
        }

    def __unicode__(self):
        return '%s:%s:%s'%(self.date, self.product.name,self.fcl_quantity)

class InventoryTransactionTruckFlow(models.Model):
    date = models.DateField(null=False)
    transaction = models.ForeignKey(InventoryTransaction, null=False, related_name='trucks')
    truck_no = models.CharField(max_length=100, null=True)
    weight_in_kg = models.FloatField(default=0.00)
    remarks = models.TextField(null=True)

    class Meta:
        db_table = 'inventory_transaction_truck_flow'


    def get_obj(self):
        return {
            'id': self.id,
            'date': self.date,
            'truckNo': self.truck_no,
            'weightInKg': self.weight_in_kg,
            'remarks': self.remarks
        }

    @classmethod
    def get_all_warehouse_butsiness_product_report(cls, business_ids=[]):
        queryset = cls.objects.filter(transaction__transaction_business__bp_id__in=business_ids)\
            .values('transaction__product__id', 'transaction__product__name').annotate(
            in_flow_all=Sum(
                Case(When(transaction__positive=True, then=F('weight_in_kg')), output_field=IntegerField())
            ),
            out_flow_all=Sum(
                Case(When(transaction__positive=False, then=F('weight_in_kg')), output_field=IntegerField())
            )
        )

        def get_total_quantity(item):
            in_flow = 0.00 if not item['in_flow_all'] else item['in_flow_all']
            out_flow = 0.00 if not item['out_flow_all'] else item['out_flow_all']
            item['totalQuantity'] = in_flow - out_flow

        map(get_total_quantity, queryset)
        return queryset

    @classmethod
    def get_product_report_for_all_warehouse(cls, own=False):
        queryset = cls.objects if own else cls.objects.filter(transaction__warehouse__self_warehouse=True)

        queryset =  queryset.values('transaction__product__id', 'transaction__product__name').annotate(
            in_flow_all=Sum(
                Case(When(transaction__positive=True, then=F('weight_in_kg')), output_field=IntegerField())
            ),
            out_flow_all=Sum(
                Case(When(transaction__positive=False, then=F('weight_in_kg')), output_field=IntegerField())
            )
        )

        def get_total_quantity(item):
            in_flow = 0.00 if not item['in_flow_all'] else item['in_flow_all']
            out_flow = 0.00 if not item['out_flow_all'] else item['out_flow_all']
            item['totalQuantity'] = in_flow - out_flow

        map(get_total_quantity, queryset)
        return queryset






    def __unicode__(self):
        return '%s:%s:%s'%(self.date, self.truck_no, self.weight_in_kg)







