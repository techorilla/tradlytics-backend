from rest_framework.permissions import IsAuthenticated, AllowAny
from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import ProductItem, ProductKeyword, ProductOrigin
from django_countries.fields import Country
import traceback


class ProductItemAPI(GenericAPIView):

    def save_product_item(self, data, user, product_item=None, update=False):
        try:
            keywords_id = data.get('keywords')
            origin = data.get('origin')
            product_id = int(data.get('productId'))
            database_ids = data.get('databaseIds')
            product_origin = ProductOrigin.objects.filter(country=Country(code=origin.upper()))\
                .get(product__id=product_id)
            keywords = ProductKeyword.objects.filter(id__in=keywords_id)

            if update:
                product_item.updated_by = user
                product_item.product_origin = product_origin
                product_item.database_ids = database_ids
                keywords_removed = product_item.keywords.exclude(id__in=keywords_id)
                # Removing Keywords
                for keyword in keywords_removed:
                    product_item.keywords.remove(keyword)
                # Adding New Keywords
                for keyword in keywords:
                    if not product_item.keywords.filter(id=keyword.id).exists():
                        product_item.keywords.add(keyword)
                product_item.save()

            else:
                product_item = ProductItem()
                product_item.product_origin = product_origin
                product_item.database_ids = database_ids
                product_item.created_by = user
                product_item.save()
                for keyword in keywords:
                    product_item.keywords.add(keyword)
                product_item.save()
            return Response({
                'success': True,
                'obj': product_item.get_obj()
            }, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        return self.save_product_item(data, user)

    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        product_item = ProductItem.objects.get(id=data.get('id'))
        return self.save_product_item(data, user, product_item=product_item, update=True)

    def get(self, request, *args, **kwargs):
        product_items = ProductItem.objects.all()
        product_items = [prod.get_obj() for prod in product_items]
        return Response({
            'data': {'productItems': product_items}
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response()





