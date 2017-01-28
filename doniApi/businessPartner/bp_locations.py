from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.businessPartner.bpLocations import BpLocation
from doniCore import Utilities


class BpLocationAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        business = Utilities.get_user_business(user)
        q = request.GET.get('q')
        if q == 'all' or q == 'drop_down':
            locations = BpLocation.objects.filter(bp=business)
            if q == 'all':
                locations = [loc.json_obj() for loc in locations]
            else:
                locations = [loc.drop_down_obj() for loc in locations]
            return Response({'locations': locations}, status=status.HTTP_200_OK)
        else:
            location = BpLocation.objects.get(id=q)
            location = location .json_obj
            return Response({'location': location}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response()

    def delete(self, request, *args, **kwargs):
        return Response()

    def put(self, request, *args, **kwargs):
        return Response()
