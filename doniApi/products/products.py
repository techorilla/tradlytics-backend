from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import ProductKeyword, Products, ProductsSpecification, Origin, ProductImage, ProductCategory
from django.db.models import Q

class ProductsImageAPI(GenericAPIView):

    # def get(self, request, *args, **kwargs):
    #     product_id = kwargs.get('product_id')
    #     image_id = kwargs.get('image_id')
    #     primary = bool(int(request.GET.get('primary', False)))
    #     print primary
    #     if product_id is not None:
    #         query = (Q(product__id=product_id) & Q(primary=True)) if primary else (Q(product__id=product_id))
    #         prod_images = ProductImages.objects.filter(query)
    #         prod_images = [{
    #             'image_id': image.id,
    #             'product_id': image.product.id,
    #             'image_url': image.image.name,
    #             'primary': image.primary
    #         } for image in prod_images]
    #         return Response({'product_images': prod_images}, status=status.HTTP_200_OK)
    #
    #     if image_id is not None:
    #         prod_image = ProductImages.objects.get(id=int(image_id))
    #         return Response({
    #             'id': prod_image.id,
    #             'product_id': product_id,
    #             'image_url': prod_image.image.name
    #         }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = kwargs.get('product_id')
        product = Products.objects.get(id=int(product_id))
        primary = bool(request.data.get('primary', False))
        image = request.FILES.get('product_image')
        prod_image = ProductImage(product=product, image=image, primary=primary)
        prod_image.created_by = user
        prod_image.save()
        return Response({
            'success': True,
            'obj': product.get_obj(),
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        image_id = kwargs.get('image_id')
        prod_image = ProductImage.objects.get(id=image_id)
        prod_image.delete()
        return Response(
            status=status.HTTP_200_OK
        )


class ProducOriginAPI(GenericAPIView):

    def post(self, request,  *args, **kwargs):
        data = request.data
        product_id = data.get('product_id')
        origins = data.get('origins')
        return Response({})


class ProductsAPI(GenericAPIView):

    def get(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        all_products = Products.objects.all()
        all_products = [product.get_obj(base_url) for product in all_products]
        return Response({'allProducts': all_products}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        base_url = request.META.get('HTTP_HOST')
        product_data = request.data.get('product')
        product_name = product_data.get('name')
        description = product_data.get('description')
        category_id = product_data.get('categoryId')
        category = ProductCategory.objects.get(id=category_id)
        new_product = Products(name=product_name)
        new_product.category = category
        new_product.created_by = user
        new_product.description = description
        new_product.save()
        return Response({
            'id': new_product.id,
            'obj': new_product.get_obj(base_url),
            'success': True,
            'message': 'Product added successfully.',
            }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id', None)
        if product_id:
            product_id = int(product_id)
            product = Products.objects.get(id=product_id)
            product.delete()
            return Response({'id': product_id}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        base_url = request.META.get('HTTP_HOST')
        product_data = request.data.get('product')
        product_id = product_data.get('id')
        product_name = product_data.get('name')
        description = product_data.get('description')
        update_product = Products.objects.get(id=product_id)
        update_product.name = product_name
        update_product.description = description
        update_product.updated_by = user
        update_product.save()
        return Response({
            'id': update_product.id,
            'obj': update_product.get_obj(base_url),
            'success': True,
            'message': 'Product updated successfully.',
            }, status=status.HTTP_200_OK)


