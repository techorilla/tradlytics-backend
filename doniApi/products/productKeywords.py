from rest_framework.permissions import IsAuthenticated, AllowAny
from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import Products, ProductKeyword, ProductCategory
from datetime import datetime as dt


class ProductsKeywordAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    messages = dict()
    messages['alreadyExist'] = 'Same keyword in this category already exist.'
    messages['successPOST'] = 'Product Keyword created successfully.'
    messages['successPUT'] = 'Product Keyword updated successfully.'

    def get(self, request, *args, **kwargs):
        keyword_id = kwargs.get('keyword_id')
        product_id = kwargs.get('productId')
        if product_id is None:
            keywords = ProductKeyword.objects.all().order_by('keyword')
            keywords = [key.get_obj() for key in keywords]
            return Response({'data':{
                'keywords': keywords
            }}, status=status.HTTP_200_OK)

    def check_keyword_already_exist(self, keyword, category_id, update_id=None):
        product_keyword = ProductKeyword.objects.filter(keyword=keyword).filter(category__id=category_id)
        if update_id:
            product_keyword.exclude(id=update_id)
        if len(product_keyword) == 0:
            return False
        else:
            return True

    def save_keyword(self, data, user):
        keyword_data = data
        keyword = keyword_data.get('name')
        update_id = keyword_data.get('id')
        category_id = keyword_data.get('categoryId')
        if not self.check_keyword_already_exist(keyword, category_id, update_id):
            category = ProductCategory.objects.get(id=category_id)
            if update_id:
                msg = self.messages['successPUT']
                product_keyword = ProductKeyword.objects.get(id=update_id)
                product_keyword.updated_by = user
                product_keyword.updated_at = dt.now()
            else:
                msg = self.messages['successPOST']
                product_keyword = ProductKeyword()
                product_keyword.created_by = user
            product_keyword.keyword = keyword
            product_keyword.category = category
            product_keyword.save()
            return Response({
                'success': True,
                'obj': product_keyword.get_obj(),
                'msg': msg
            }, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': self.messages['alreadyExist']},
                            status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        return self.save_keyword(request.data, user)

    def delete(self, request, *args, **kwargs):
        keyword_id = kwargs.get('id')
        product_keyword = ProductKeyword.objects.get(id=keyword_id)
        product_keyword.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        return self.save_keyword(request.data, user)