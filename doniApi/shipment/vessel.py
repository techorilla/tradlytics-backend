from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import Vessel
from django.db.models import Q
from datetime import datetime as dt


class VesselListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        search_obj = request.data.get('searchObj')
        query_type = search_obj.get('queryType')
        query = search_obj.get('query')


        if query_type == 'imo_number':
            all_vessel = Vessel.objects.filter(Q(imo_number__istartswith=query))
        elif query_type == 'mmsi_number':
            all_vessel = Vessel.objects.filter(Q(mmsi_number__istartswith=query))
        elif query_type == 'vessel_name':
            all_vessel = Vessel.objects.filter(Q(first_name__icontains=query))
        elif query_type == 'line':
            all_vessel = Vessel.objects.filter(Q(operator__istartswith=query) | Q(shipping_line__name__icontains=query)
                                               | Q(shipping_line__code_name__istartswith=query))
        else:
            all_vessel = []


        all_vessel = [vessel.get_list_obj(base_url) for vessel in all_vessel]
        return Response({
            'list': all_vessel,
            'success': True

        }, status=status.HTTP_200_OK)


class VesselTagAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        if query:
            vessel_tags = Vessel.objects.filter(Q(first_name__icontains=query)| Q(imo_number__istartswith=query)
                                                | Q(mmsi_number__istartswith=query))\
                .values('first_name', 'imo_number', 'id', 'mmsi_number').order_by('name')
        else:
            vessel_tags = []



        # vessel_tags = [tag.get('name') for tag in vessel_tags]
        return Response({'data': vessel_tags}, status=status.HTTP_200_OK)


class VesselAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def save_vessel(self, request, action='added'):
        print action, request.data
        try:
            success_msg = 'Vessel %s successfully!'
            vessel_data = request.data.get('vesselObj')
            print vessel_data
            user = request.user
            id = vessel_data.get('id')
            name = vessel_data.get('name')
            imo_number = vessel_data.get('imoNumber')
            mmsi = vessel_data.get('mmsi')
            line_id = vessel_data.get('shippingLineId')

            if id:
                vessel = Vessel.objects.get(id=id)
                vessel.updated_by = user
                vessel.updated_at = dt.now()
            else:
                vessel = Vessel()
                vessel.created_by = user

            vessel.imo_number = imo_number
            vessel.mmsi_number = mmsi
            vessel.first_name = name

            if line_id:
                vessel.shipping_line_id = line_id

            vessel.save()
            return Response({
                'success': True,
                'message': success_msg%action
            }, status=status.HTTP_200_OK)

        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })







    def get(self, request, *args, **kwargs):

        vessel_id = request.GET.get('id')
        vessel = Vessel.objects.get(id=vessel_id)
        return Response({
            'vesselObj': vessel.get_complete_obj()
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.save_vessel(request)

    def put(self, request, *args, **kwargs):
        return self.save_vessel(request, action='updated')

    def delete(self, request, *args, **kwargs):
        try:
            vessel_id = request.GET.get('vessel_id')
            vessel = Vessel.objects.get(id=vessel_id)
            name = vessel.first_name
            vessel.delete()
            return Response({
                'success': True,
                'message': 'Vessel %s deleted successfully'%name
            }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })