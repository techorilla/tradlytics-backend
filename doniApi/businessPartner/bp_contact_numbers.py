from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.businessPartner.bpContactNumbers import BpContactNumber, BpBasic
from datetime import datetime as dt


class BpContactNumberAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    messages = dict()
    messages['errorPOST'] = 'Business contact numbers were not added due to some error on server.'
    messages['successPOST'] = 'Business contact numbers updated successfully.'

    def get(self, request, *args, **kwargs):
        return Response({})

    def post(self, request, *args, **kwargs):
        try:
            business_id = request.data.get('bpId')
            business = BpBasic.objects.get(bp_id=business_id)
            contact_data = request.data.get('contacts')
            cont_ids = [int(cont.get('id')) for cont in contact_data if cont.get('id') is not None]
            # delete first
            business.contacts.exclude(id__in=cont_ids).delete()

            for cont in contact_data:
                cont_id = cont.get('id')
                # edit
                if cont_id:
                    contact = BpContactNumber.objects.get(id=cont_id)
                    contact.updated_by = request.user
                    contact.updated_at = dt.now()
                # new
                else:
                    contact = BpContactNumber()
                    contact.bp = business
                    contact.created_by = request.user
                contact.contact_number = cont.get('contactNumber')
                contact.type = cont.get('contactType')
                contact.save()
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
