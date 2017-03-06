from rest_framework.permissions import IsAuthenticated, AllowAny
from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import ProductCategory
from datetime import datetime as dt
from django.db import IntegrityError


class ProductsCategoryAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    messages = dict()
    messages['alreadyExist'] = 'This product category already exist.'
    messages['successPOST'] = 'Product category created successfully.'
    messages['successPUT'] = 'Product category updated successfully.'

    def get(self, request, *args, **kwargs):
        categories = ProductCategory.objects.all().order_by('name')
        categories = [cat.get_obj() for cat in categories]
        return Response({'allCategories': categories}, status=status.HTTP_200_OK)

    def save_category(self, data, user):
        update_id = data.get('id')
        name = data.get('name')
        description = data.get('description')
        try:
            if update_id:
                category = ProductCategory.objects.get(id=update_id)
                category.updated_by = user
                category.updated_at = dt.now()
                msg = self.messages['successPUT']
            else:
                category = ProductCategory()
                category.created_by = user
                msg = self.messages['successPOST']
            category.name = name
            category.description = description
            category.save()
            return Response({
                'success': True,
                'message': msg,
                'obj': category.get_obj()
            }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({'success': False, 'message': self.messages['alreadyExist']})

    def post(self, request, *args, **kwargs):
        return self.save_category(request.data, request.user)

    def put(self, request, *args, **kwargs):
        return self.save_category(request.data, request.user)

    def delete(self, request, *args, **kwargs):
        data = request.data
        id = data.get('id')
        cat = ProductCategory.objects.get(id=id)
        if cat.product_count == 0:
            cat.delete()
            return Response({'success': True,  'message': 'Category successfully delete.'})
        else:
            return Response({
                'success': False,
                'message': 'Some Products are associated with these products, hence can not be deleted.'
            })



