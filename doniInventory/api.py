from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import Origin
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Warehouse, WarehouseRent, InventoryTransaction, InventoryTransactionTruckFlow
from datetime import datetime as dt
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

class InventoryTransactionAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response()

class InventoryDashboardAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'data': {}
        }, status=status.HTTP_200_OK)




