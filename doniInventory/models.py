from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from doniServer.models import Products, BpBasic
from django.contrib.auth.models import User
from datetime import timedelta

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
            'consumedCapacity': 'NA',
            'rentPer50Kg': rent_per_50kg
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
    warehouse = models.ForeignKey(Warehouse, null=False)
    lot_no = models.IntegerField(default=1)
    date = models.DateField(null=False)
    transaction_business = models.ForeignKey(BpBasic, null=True, on_delete=models.SET_NULL)
    port_clearing_no = models.CharField(max_length=50, null=True)
    fcl_quantity = models.IntegerField(default=0.00)
    product = models.ForeignKey(Products, null=False)
    positive = models.BooleanField(default=True)

    class Meta:
        db_table = 'inventory_transaction'

    def __unicode__(self):
        return '%s:%s:%s'%(self.date, self.product.name,self.fcl_quantity)


class InventoryTransactionTruckFlow(models.Model):
    date = models.DateField(null=False)
    truck_no = models.CharField(max_length=100, null=True)
    weight_in_kg = models.FloatField(default=0.00)
    remarks = models.TextField(null=True)

    class Meta:
        db_table = 'inventory_transaction_truck_flow'

    def __unicode__(self):
        return '%s:%s:%s'%(self.date, self.truck_no, self.weight_in_kg)







