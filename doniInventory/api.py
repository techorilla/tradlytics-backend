from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import Origin
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Warehouse, WarehouseRent, InventoryTransaction, InventoryTransactionTruckFlow
from datetime import datetime as dt
from django.db.models import Sum, Count
import dateutil.parser


class WarehouseListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        all_warehouses = Warehouse.objects.filter(business=request.user.profile.business)
        all_warehouses = [warehouse.get_warehouse_list_obj() for warehouse in all_warehouses]

        return Response({
            'list': all_warehouses
        }, status=status.HTTP_200_OK)


class WarehouseAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request, *args, **kwargs):
        warehouse_id = request.GET.get('id')
        with_rent = request.GET.get('rent', False)
        warehouse = Warehouse.objects.get(id=warehouse_id)
        return Response({
            'success':True,
            'warehouseObj': warehouse.get_complete_obj(with_rent=with_rent)
        })

    def put(self, request, *args, **kwargs):
        return self.save_warehouse(request.data, request.user, request.method)

    def post(self, request, *args, **kwargs):
        return self.save_warehouse(request.data, request.user, request.method)

    def delete(self, request, *args, **kwargs):
        return Response()

    def save_warehouse(self, data, user, method):
        try:
            message = 'Warehouse %s %s successfully.'
            id = data.get('id')
            name = data.get('name')
            lots = int(data.get('lots'))
            total_capacity_in_kgs = float(data.get('totalCapacity'))
            self_ware_house = data.get('selfWarehouse')
            contact = data.get('contact')
            address = data.get('address')
            if  method == 'POST':
                warehouse = Warehouse()
                warehouse.created_by = user
            else:
                warehouse = Warehouse.objects.get(id=id)
                warehouse.updated_by = user
                warehouse.updated_at = dt.now()
            warehouse.name = name
            warehouse.lots = lots
            warehouse.self_warehouse = self_ware_house
            warehouse.total_capacity_kgs = total_capacity_in_kgs
            warehouse.business = user.profile.business
            warehouse.address = address
            warehouse.contact = contact
            action = 'created' if method == 'POST' else 'updated'
            message = message%(action, name)
            warehouse.save()
            return Response({
                'id': warehouse.id,
                'success': True,
                'message': message
            }, status=status.HTTP_200_OK)

        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })




class WarehouseRentAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        warehouse_id = data.get('warehouseId')
        rent = data.get('rent')
        date_change = data.get('dateChange')
        date_change = dateutil.parser.parse(date_change)
        date_change = date_change.replace(hour=0, minute=0, second=0, microsecond=0)
        warehouse = Warehouse.objects.get(id=warehouse_id)
        last_date = WarehouseRent.get_last_warehouse_rent_date(warehouse_id)

        if last_date:
            if date_change.date() < last_date:
                return Response({
                    'success': False,
                    'message': 'Price already exist for this date'
                })

        new_rent = WarehouseRent()
        new_rent.warehouse_id = warehouse_id
        new_rent.created_by = request.user
        new_rent.date_change = date_change
        new_rent.rent = rent
        new_rent.update_last_warehouse_rent()
        new_rent.save()


        return Response({
            'rentList': [rent.get_list_obj() for rent in warehouse.warehouse_rent.all()],
            'success': True,
            'message': 'Warehouse new rent added successfully.'
        }, status=status.HTTP_200_OK)

class InventoryTransactionListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        business = request.user.profile.business
        start_date = request.GET.get(u'startDate')
        end_date = request.GET.get(u'endDate')
        start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
        end_date = dateutil.parser.parse(str(end_date).replace('"', ''))
        all_inventory_transactions = InventoryTransaction.objects\
            .filter(date__lte=end_date).filter(date__gte=start_date)\
            .filter(created_by__profile__business=business) \
            .annotate(total_weight_in_kgs=Sum('trucks__weight_in_kg')).annotate(total_trucks=Count('trucks')) \
            .order_by('-date')\
            .values('id','date','warehouse__id', 'warehouse__name', 'lot_no', 'fcl_quantity', 'positive', 'product__id', 'product__name',
                    'total_weight_in_kgs','total_trucks', 'transaction_business__bp_id', 'transaction_business__bp_name')
        return Response({
            'list': all_inventory_transactions
        }, status=status.HTTP_200_OK)


class InventoryTransactionAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        inventory_record_id = request.GET.get('id')
        record = InventoryTransaction.objects.get(id=inventory_record_id)
        return Response({
            'success': True,
            'recordObj': record.get_complete_obj()
        }, status=status.HTTP_200_OK)

    def save_inventory_transaction(self, request):
        inventory_data = request.data
        inventory_record_id = inventory_data.get('id', None)
        business_id = inventory_data.get('businessId')
        warehouse_id = inventory_data.get('warehouseId')
        lot_no = inventory_data.get('lotNo')
        port_clearing_no = inventory_data.get('portClearingNo')
        fcl_quantity = inventory_data.get('fclQuantity')
        product_id = inventory_data.get('productId')
        positive =  inventory_data.get('positive')
        trucks = inventory_data.get('trucks')
        removed_trucks = inventory_data.get('removedTrucks', [])
        removed_trucks = [int(id) for id in removed_trucks]
        try:
            inventory_record = InventoryTransaction.objects.get(id=inventory_record_id)
        except InventoryTransaction.DoesNotExist:
            print inventory_record_id
            inventory_record = InventoryTransaction()

        if inventory_record_id:
            message = 'Inventory Record Updated Successfully'
            inventory_record.updated_by = request.user
            inventory_record.updated_at = dt.now()
        else:
            message = 'Inventory Record Added Successfully'
            inventory_record.created_by = request.user

        date = inventory_data.get('date')
        date = dateutil.parser.parse(date)
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        inventory_record.lot_no = lot_no
        inventory_record.date = date
        inventory_record.transaction_business_id = business_id
        inventory_record.port_clearing_no = port_clearing_no
        inventory_record.fcl_quantity = fcl_quantity
        inventory_record.product_id = product_id
        inventory_record.positive = positive
        inventory_record.warehouse_id = warehouse_id
        inventory_record.save()

        # Save New Trucks
        new_trucks = [truck for truck in trucks if truck.get('id')=='new']
        for truck in new_trucks:
            truck_flow_date = truck.get('date')
            truck_flow_date = dateutil.parser.parse(truck_flow_date)
            truck_flow_date = truck_flow_date.replace(hour=0, minute=0, second=0, microsecond=0)
            new_truck = InventoryTransactionTruckFlow()
            new_truck.date = truck_flow_date
            new_truck.truck_no = truck.get('truckNo')
            new_truck.weight_in_kg = truck.get('weightInKg')
            new_truck.remarks = truck.get('remarks')
            new_truck.transaction = inventory_record
            new_truck.save()

        # Save Edited Trucks
        old_trucks = [truck for truck in trucks if truck.get('id') != 'new']

        for truck in old_trucks:
            old_truck = InventoryTransactionTruckFlow.objects.get(id=truck.get('id'))
            truck_flow_date = truck.get('date')
            truck_flow_date = dateutil.parser.parse(truck_flow_date)
            truck_flow_date = truck_flow_date.replace(hour=0, minute=0, second=0, microsecond=0)
            old_truck.date = truck_flow_date
            old_truck.truck_no = truck.get('truckNo')
            old_truck.weight_in_kg = truck.get('weightInKg')
            old_truck.remarks = truck.get('remarks')
            old_truck.transaction = inventory_record
            old_truck.save()

        # Delete Removed Truck
        if len(removed_trucks):
            InventoryTransactionTruckFlow.objects.filter(id__in=removed_trucks).delete()

        return Response({
            'success':True,
            'message': message
        })



    def post(self, request, *args, **kwargs):
        return self.save_inventory_transaction(request)

    def put(self, request, *args, **kwargs):
        return self.save_inventory_transaction(request)

class InventoryDashboardAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        business = user.profile.business
        all_business_ids = business.app_profile.all_associated_companies_id
        total_warehouse = Warehouse.objects.count()
        owned_warehouse = Warehouse.objects.filter(self_warehouse=True).count()
        all_warehouses = Warehouse.objects.all()
        all_warehouses = [warehouse.dashboard_warehouse_card() for warehouse in all_warehouses]
        all_warehouse_product = InventoryTransactionTruckFlow.get_product_report_for_all_warehouse()
        own_warehouse_product = InventoryTransactionTruckFlow.get_product_report_for_all_warehouse(own=True)
        business_product_report = InventoryTransactionTruckFlow.get_all_warehouse_butsiness_product_report(business_ids=all_business_ids)


        return Response({
            'data': {
                'totalWarehouseCount': total_warehouse,
                'ownedWarehouseCount': owned_warehouse,
                'allWarehouse':all_warehouses,
                'allWarehousesProduct': all_warehouse_product,
                'ownWarehouseProduct': own_warehouse_product,
                'businessProductReport': business_product_report
            }
        }, status=status.HTTP_200_OK)

class WarehouseProductReportAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        warehouse_id = request.GET.get('warehouseId')
        warehouse = Warehouse.objects.get(id=warehouse_id)
        user = request.user
        business = user.profile.business
        all_products= warehouse.record.all().values('product__id', 'product__name').distinct()
        all_associated_ids = business.app_profile.all_associated_companies_id

        product_report = []

        for product in all_products:
            product_report.append(warehouse.get_product_report(all_associated_ids, product.get('product__id'), product.get('product__name')))

        return Response({
            'productReport': product_report
        }, status=status.HTTP_200_OK)

class WarehouseBusinessReportAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            warehouse_id = request.GET.get('warehouseId')
            warehouse = Warehouse.objects.get(id=warehouse_id)
            all_business = warehouse.record.all().values('transaction_business__bp_id', 'transaction_business__bp_name').distinct()
            business_report = []
            print all_business

            for business in all_business:
                business_report.append(warehouse.get_business_product_report(business.get('transaction_business__bp_id'), business.get('transaction_business__bp_name')))

            return Response({
                'businessReport': business_report
            }, status=status.HTTP_200_OK)
        except Exception, e:
            import traceback
            traceback.print_exc()