from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime as dt
from doniServer.models import BpBasic


class BusinessSettingsAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            business = user.profile.business
            data = request.data
            website = data.get('website')
            business.bp_website = website
            business.save()
            return Response({
                'success': True,
                'message': 'Business details updated successfully!'
            },status=status.HTTP_200_OK)
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })