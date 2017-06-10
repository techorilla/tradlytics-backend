from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import ShippingPort


class ShippingPortAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        all_ports = ShippingPort.objects.all()
        all_ports = [port.get_obj() for port in all_ports]

        return Response({
            'allPorts': all_ports
        }, status=status.HTTP_200_OK)

