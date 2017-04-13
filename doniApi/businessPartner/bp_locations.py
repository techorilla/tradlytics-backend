from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.businessPartner.bpLocations import BpLocation, BpBasic
from doniCore import Utilities
from datetime import datetime as dt


class BpLocationAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    messages = dict()
    messages['errorPOST'] = 'Business locations were not added due to some error on server.'
    messages['successPOST'] = 'Business locations added successfully.'

    def get(self, request, *args, **kwargs):
        user = request.user
        business = Utilities.get_user_business(user)
        q = request.GET.get('q')
        if q == 'all' or q == 'drop_down':
            locations = BpLocation.objects.filter(bp=business)
            if q == 'all':
                locations = [loc.get_obj() for loc in locations]
            else:
                locations = [loc.drop_down_obj() for loc in locations]
            return Response({'locations': locations}, status=status.HTTP_200_OK)
        else:
            location = BpLocation.objects.get(id=q)
            location = location.get_obj()
            return Response({'location': location}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            business_id = request.data.get('bpId')
            business = BpBasic.objects.get(bp_id=business_id)

            locations_data = request.data.get('locations')
            loc_ids = [int(loc.get('id')) for loc in locations_data if loc.get('id') is not None]
            # delete first
            business.locations.exclude(address_id__in=loc_ids).delete()

            for loc in locations_data:
                loc_id = loc.get('id')
                # edit
                if loc_id:
                    location = BpLocation.objects.get(address_id=loc_id)
                    location.updated_by = request.user
                    location.updated_at = dt.now()
                # new
                else:
                    location = BpLocation()
                    location.bp = business
                    location.created_by = request.user
                location.is_primary = loc.get('isPrimary')
                location.address = loc.get('address')
                location.city = loc.get('city')
                location.state = loc.get('state')
                location.country = loc.get('country')
                location.is_primary = loc.get('isPrimary')
                location.save()
            return Response({
                'success': True,
                'message': self.messages['successPOST']
            }, status=status.HTTP_200_OK)
        except Exception, e:
            print str(e)
            return Response({
                'success': False,
                'message': self.messages['errorPOST']
            })
