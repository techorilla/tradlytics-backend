from rest_framework.permissions import IsAuthenticated, AllowAny
from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import Products, ProductKeyword


class ProductsKeywordAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        keyword_id = kwargs.get('keyword_id')
        product_id = kwargs.get('product_id')
        if keyword_id is None and product_id is None:
            all_keywords = ProductKeyword.objects.all()
            all_keywords = [{
                                'id': key.id,
                                'name': key.keyword
                            } for key in all_keywords]

            return Response({'all_keywords': all_keywords}, status=status.HTTP_200_OK)
        elif product_id:
            product = Products.objects.filter(id=product_id)
            all_keywords = product.quality_keywords.all()
            all_keywords = [{
                                'id': key.id,
                                'name': key.name
                            } for key in all_keywords]

            return Response({'all_keywords': all_keywords}, status=status.HTTP_200_OK)
        else:
            keyword = ProductKeyword.objects.get(id=keyword_id)

            return Response({
                'id': keyword.id,
                'keyword': keyword.keyword
            }, status=status.HTTP_200_OK)

    def check_keyword_already_exist(self, keyword):
        product_keyword = ProductKeyword.objects.filter(keyword=keyword)
        if len(product_keyword) == 0:
            return False
        else:
            return True

    def post(self, request, *args, **kwargs):
        keyword_data = request.data
        user = request.user
        keyword = keyword_data.get('keyword')
        if not self.check_keyword_already_exist(keyword):
            product_keyword = ProductKeyword(keyword=keyword_data.get('keyword'))
            product_keyword.created_by = user
            product_keyword.save()
            return Response({'id': product_keyword.id}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_409_CONFLICT)

    def delete(self, request, *args, **kwargs):
        keyword_id = kwargs.get('id')
        product_keyword = ProductKeyword.objects.get(id=keyword_id)
        product_keyword.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        keyword_id = kwargs.get('id')
        keyword_data = request.data
        product_keyword = ProductKeyword.objects.get(id=keyword_id)
        product_keyword.name = keyword_data.get('keyword')
        product_keyword.save()
        return Response(status=status.HTTP_200_OK)