from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.businessPartner.bpContacts import BpContact, BpBasic
from datetime import datetime as dt

class BpContactPersonAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    messages = dict()
    messages['errorPOST'] = 'Business contact persons were not added due to some error on server.'
    messages['successPOST'] = 'Business contact persons updated successfully.'

    def get(self, request, *args, **kwargs):
        return Response({})

    def post(self, request, *args, **kwargs):
        try:
            business_id = request.data.get('bpId')
            business = BpBasic.objects.get(bp_id=business_id)
            contact_persons_data = request.data.get('contactPersons')
            cont_per_ids = [int(contPer.get('id')) for contPer in contact_persons_data if contPer.get('id') is not None]
            # delete first
            business.contact_persons.exclude(id__in=cont_per_ids).delete()

            for cont_per in contact_persons_data:
                cont_per_id = cont_per.get('id')
                # edit
                if cont_per_id:
                    contact_person = BpContact.objects.get(id=cont_per_id)
                    contact_person.updated_by = request.user
                    contact_person.updated_at = dt.now()
                # new
                else:
                    contact_person = BpContact()
                    contact_person.bp = business
                    contact_person.created_by = request.user
                contact_person.is_primary = cont_per.get('isPrimary')
                contact_person.full_name = cont_per.get('fullName')
                contact_person.designation = cont_per.get('designation')
                contact_person.email = cont_per.get('email')
                contact_person.primary_number = cont_per.get('primaryNumber')
                contact_person.secondary_number = cont_per.get('secondaryNumber')
                contact_person.save()
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
