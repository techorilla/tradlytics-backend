from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.dropDowns import *
from django.utils import timezone
from doniCore import Utilities


class SimpleDropDownAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        business = Utilities.get_user_business(user)
        print request.GET
        q = request.GET.get('q')
        if q == 'all' or q == 'drop_down':
            result_objects = self.model.objects.filter(business=business)
            if q == 'all':
                results = [res.get_list_obj() for res in result_objects]
            else:
                results = [res.drop_down_obj() for res in result_objects]
            return Response({'list': results}, status=status.HTTP_200_OK)
        else:
            result_object = self.model.objects.get(id=int(q))
            return Response({'object': result_object.get_list_obj()}, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        user = request.user
        id = request.data.get('id')
        name = request.data.get('name')
        drop_down_obj = self.model.objects.get(id=id)
        drop_down_obj.name = name
        drop_down_obj.updated_by = user
        drop_down_obj.updated_at = timezone.now()
        drop_down_obj.save()
        return Response({'obj': drop_down_obj.get_list_obj()}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        business = Utilities.get_user_business(user)
        name = request.data.get('name')
        drop_down_obj = self.model.objects.create(
            name=name,
            created_at=timezone.now(),
            created_by=user,
            updated_at=None,
            business=business
        )
        return Response({'obj': drop_down_obj.get_list_obj()}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        id = request.data.get('id')
        drop_down_obj = self.model.objects.get(id=id)
        drop_down_obj.delete()
        return Response({'id': id}, status=status.HTTP_200_OK)


class BusinessTypeAPI(SimpleDropDownAPI):
    model = BusinessType


class ContactType(SimpleDropDownAPI):
    model = ContactType


class ContractType(SimpleDropDownAPI):
    model = TransactionContractType


class Designation(SimpleDropDownAPI):
    model = Designation


class ProductQuality(SimpleDropDownAPI):
    model = ProductQuality


class TransactionStatus(SimpleDropDownAPI):
    model = TransactionStatus








