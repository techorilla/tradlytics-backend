from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import ShippingLine
from datetime import datetime as dt
from doniCore.utils import Utilities
import json, os


class ShippingLineListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        shipping_line = ShippingLine.objects.all()
        shipping_line = [line.get_list_obj(base_url) for line in shipping_line]
        return Response({
            'list':shipping_line,
            'success': True
        }, status=status.HTTP_200_OK)


class ShippingLineAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    messages = dict()
    messages['errorPOST'] = 'Shipping Line was not created due to some error on server.'
    messages['successPOST'] = 'Shipping Line created successfully.'
    messages['successPUT'] = 'Shipping Line Information updated successfully.'
    messages['errorPUT'] = 'Shipping Line Information not updated due to some error on server.'

    def get(self, request, *args, **kwargs):
        shipping_line_id = request.GET.get('shippingLineId')[0]
        base_url = request.META.get('HTTP_HOST')
        line = ShippingLine.objects.get(id=shipping_line_id)
        return Response({
            'success': True,
            'shippingLineObj': line.get_complete_obj(base_url)
        }, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        return self.save_shipping_line(request)

    def put(self, request, *args, **kwargs):
        return self.save_shipping_line(request)

    def delete(self, request, *args, **kwargs):
        try:
            line_id = kwargs.get('line_id')
            print line_id
            line = ShippingLine.objects.get(id=line_id)
            vessel_exists = line.vessels.exists()
            line_name = line.name
            if not vessel_exists:
                line.delete()

                return Response({
                    'success': True,
                    'message': 'Shipping line %s deleted successfully'%line_name
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'success': False,
                    'message': 'Can not delete Shipping Line %s as it has vessels associated with it!'
                })
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })


    def save_shipping_line(self, request):
        try:

            line_logo = request.FILES.get('logo')
            line_data = json.loads(request.data.get('lineData'))

            line_id = line_data.get('id')
            code_name = line_data.get('codeName')
            name = line_data.get('name')
            website = line_data.get('website')
            tracking_website = line_data.get('trackingWebsite')

            if line_id:
                line = ShippingLine.objects.get(id=line_id)
                line.updated_by = request.user
                line.updated_at = dt.now()
                if line_logo:
                    if line.logo:
                        path = Utilities.get_media_directory()+'/'+str(line.logo)
                        os.remove(path)
                    line.logo = line_logo
                success_message = self.messages['successPUT']
            else:
                line = ShippingLine()
                line.created_by = request.user
                if line_logo:
                    line.logo = line_logo
                success_message = self.messages['successPOST']

            line.code_name = code_name
            line.name = name
            line.website = website
            line.tracking_website = tracking_website
            line.save()

            return Response({
                'success': True,
                'message': success_message
            }, status=status.HTTP_200_OK)

        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_200_OK)




