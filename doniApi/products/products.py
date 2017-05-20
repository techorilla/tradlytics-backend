from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import ProductKeyword, Products, ProductsSpecification, ProductOrigin, ProductCategory
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniCore.utils import Utilities
import os, json
from datetime import datetime as dt
from django_countries.fields import Country
from doniCore.cache import cache


class ProducOriginAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,  *args, **kwargs):
        data = request.data
        product_id = data.get('product_id')
        origins = data.get('origins')
        product = Products.objects.get(id=int(product_id))
        product_origins = [org.country.code for org in product.origins]

        for origin_code in origins:
            if origin_code not in product_origins:
                new_origin = ProductOrigin()
                new_origin.product = product
                new_origin.country = Country(code=origin_code)
                new_origin.save()
            else:
                product_origins.remove(origin_code)

        message = 'Product origins updated successfully.'

        for origin_code in product_origins:
            country = Country(code=origin_code)
            delete_origin = ProductOrigin.objects.get(product=product, country=country)
            origin_items = delete_origin.origin_product_item.count()
            if origin_items == 0:
                delete_origin.delete()
            else:
                message = message + ' ' + str(country.name) + ' was not deleted as it has a product item.'
        return Response({
            'success': True,
            'message': message
        }, status=status.HTTP_200_OK)


class ProductTagsAPI(GenericAPIView):

    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('productId')
        query = request.GET.get('query')
        product_tags = None
        if product_id:
            product_tags = Products.objects.exclude(id=int(product_id))\
                .filter(name__icontains=query)\
                .values('id','name',  'category__name').order_by('name')
        else:
            product_tags = Products.objects.filter(name__icontains=query) \
                .values('id','name', 'category__name').order_by('name')
        print product_tags
        product_tags = [{
                            'id': tag.get('id'),
                            'name':tag.get('name'),
                            'category': tag.get('category__name')
                        }for tag in product_tags]

        return Response(product_tags, status=status.HTTP_200_OK)



class ProductOnWebsiteAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            product_id = request.data.get('productId')
            status = request.data.get('status')
            product = Products.objects.get(id=product_id)
            product.on_website = status
            product.save()
            if status:
                message = product.name + 'is now being displayed on website.'
            else:
                message = product.name + 'is removed from website display.'

            return Response({'success': True, 'message': message})
        except Exception, e:
            return Response({'success': False, 'message': str(e)})

class ProductsAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    messages = dict()
    messages['errorPOST'] = 'Product was not created due to some error on server.'
    messages['successPOST'] = 'Product created successfully.'
    messages['successPUT'] = 'Product Information updated successfully.'
    messages['errorPUT'] = 'Product Information not updated due to some error on server.'

    def get(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        all_products = Products.objects.all()
        all_products = [product.get_obj(base_url) for product in all_products]
        return Response({'allProducts': all_products}, status=status.HTTP_200_OK)

    def save_related_products(self, product, related_product=[]):
        related_product_id = [int(prod.get(u'id')) for prod in related_product]
        product_removed = product.related_products.exclude(id__in=related_product_id)
        related_product = Products.objects.filter(id__in=related_product_id)
        ## Removing removed related products
        for prod in product_removed:
            product.related_products.remove(prod)
        ## Adding new related products
        for prod in related_product:
            if not product.related_products.filter(id=prod.id).exists():
                product.related_products.add(prod)
        product.save()


    def save_product(self, request):
        try:
            user = request.user
            base_url = request.META.get('HTTP_HOST')
            product_image = request.FILES.get('image')
            product_data = json.loads(request.data.get('product'))
            product_id = product_data.get('id')
            product_name = product_data.get('name')
            product_description = product_data.get('description')
            product_category_id = product_data.get('categoryId')
            product_code = product_data.get('productCode')
            related_product = product_data.get('relatedProduct')

            if product_id:
                success_message = self.messages['successPUT']
                error_message = self.messages['errorPUT']
                product = Products.objects.get(id=product_id)
                product.updated_by = user
                product.updated_at = dt.now()
                if product.image and product_image:
                    path = Utilities.get_media_directory() + '/' + str(product.image)
                    os.remove(path)
            else:
                success_message = self.messages['successPOST']
                error_message = self.messages['errorPOST']
                product = Products()
                product.created_by = request.user

            if product_image:
                product.image = product_image
            product.name = product_name
            product.description = product_description
            product.category = ProductCategory.objects.get(id=int(product_category_id))
            product.product_code = product_code
            product.save()
            self.save_related_products(product, related_product)
            cache.delete('get_product_drop_down')
            return Response({
                'success': True,
                'message': success_message,
                'id': product.id,
            }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.save_product(request)

    def delete(self, request, *args, **kwargs):
        try:
            product_id = kwargs.get('product_id', None)
            if product_id:
                product_id = int(product_id)
                product = Products.objects.get(id=product_id)
                product.delete()
                cache.delete('get_product_drop_down')
                return Response({
                    'id': product_id,
                    'success': True,
                    'message': product.name + ' delete successfully.'
                }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })

    def put(self, request, *args, **kwargs):
        return self.save_product(request)



