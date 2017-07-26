from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from doniServer.models import Products, BpBasic
from django.contrib.auth.models import User
from datetime import timedelta
from django.db.models import Sum

# Create your models here.


class Warehouse(models.Model):

    name = models.CharField(max_length=200)
    lots = models.IntegerField(default=0)
    address = models.TextField()
    contact = models.TextField()
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
            'lots': self.lots,
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
            'lots': self.lots,
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
    lot_no = models.IntegerField(default=1)
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

    def __unicode__(self):
        return '%s:%s:%s'%(self.date, self.truck_no, self.weight_in_kg)







