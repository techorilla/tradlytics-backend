from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import ShippingPort
import pycountry
from datetime import datetime as dt


class ShippingPortListAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        all_ports = ShippingPort.objects.all()
        all_ports = [port.get_obj() for port in all_ports]

        return Response({
            'allPorts': all_ports
        }, status=status.HTTP_200_OK)


class ShippingPortAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        port_id = kwargs.get('port_id')
        port = ShippingPort.objects.get(id=port_id)
        return Response({
            'portObj':port.get_obj(),
            'success': True
        }, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        try:

            user = request.user
            port_obj = request.data.get('portObj')
            port_id = port_obj.get('id')
            country_code = port_obj.get('countryCode')
            country = pycountry.countries.get(alpha_2=country_code)
            name = port_obj.get('name')
            lo_code = port_obj.get('loCode')
            contact_no = port_obj.get('contactNo')
            website = port_obj.get('website')

            port = ShippingPort.objects.get(id=port_id)

            port.country = country.name
            port.lo_code = lo_code
            port.contact_no = contact_no
            port.website = website
            port.name = name
            port.updated_by = user
            port.updated_at = dt.now()
            port.save()

            return Response({
                'portObj': port.get_obj(),
                'success': True,
                'message': 'Shipping Port %s updated successfully' % (name)
            })

        except Exception, e:
            return  Response({
                'message': str(e),
                'success': False
            })




    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            port_obj = request.data.get('portObj')
            country_code = port_obj.get('countryCode')
            country =  pycountry.countries.get(alpha_2=country_code)
            name = port_obj.get('name')
            lo_code = port_obj.get('loCode')
            contact_no = port_obj.get('contactNo')
            website =  port_obj.get('website')

            new_port = ShippingPort()

            new_port.country = country.name
            new_port.name = name
            new_port.lo_code = lo_code
            new_port.contact_no = contact_no
            new_port.website = website
            new_port.created_by = user
            new_port.save()
            return Response({
                'portObj': new_port.get_obj(),
                'success': True,
                'message': 'Shipping Port %s created successfully' % (name)
            }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })

    def delete(self, request, *args, **kwargs):
        port_id = kwargs.get('port_id')
        port = ShippingPort.objects.get(id=port_id)
        port_name = port.name
        port.delete()
        return Response({
            'success': True,
            'message': 'Port %s deleted successfully.'%port_name
        }, status=status.HTTP_200_OK)



