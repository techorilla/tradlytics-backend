from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.businessPartner.bpBank import BpBank, BpBasic
from datetime import datetime as dt


class BpBankAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    messages = dict()
    messages['errorPOST'] = 'Business banks were not added due to some error on server.'
    messages['successPOST'] = 'Business banks updated successfully.'

    def get(self, request, *args, **kwargs):
        return Response({})

    def post(self, request, *args, **kwargs):
        try:
            business_id = request.data.get('bpId')
            business = BpBasic.objects.get(bp_id=business_id)
            banks = request.data.get('banks')
            bank_ids = [int(bank.get('id')) for bank in banks if bank.get('id') is not None]
            # delete first
            business.banks.exclude(acc_id__in=bank_ids).delete()

            for bp_bank in banks:
                bank_id = bp_bank.get('id')
                # edit
                if bank_id:
                    bank = BpBank.objects.get(acc_id=bank_id)
                    bank.updated_by = request.user
                    bank.updated_at = dt.now()
                # new
                else:
                    bank = BpBank()
                    bank.bp = business
                    bank.created_by = request.user
                bank.branch_address = bp_bank.get('accountAddress')
                bank.bank_name = bp_bank.get('bankName')
                bank.acc_title = bp_bank.get('accountTitle')
                bank.acc_number = bp_bank.get('accountNumber')
                bank.acc_country = bp_bank.get('accountCountry')
                bank.acc_city = bp_bank.get('accountCity')
                bank.save()
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
