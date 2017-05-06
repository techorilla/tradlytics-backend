from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import ProductsSpecification, ProductCategory
from datetime import datetime as dt

class ProductSpecificationAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('categoryId')
        data = dict()
        category = ProductCategory.objects.get(id=int(category_id))
        data['categoryId'] = category_id
        data['categoryName'] = category.name
        try:
            data['specs'] = ProductsSpecification.objects.get(productCategory=category).specs
        except ProductsSpecification.DoesNotExist:
            data['specs'] = []

        return Response({
            'data': data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            data=request.data
            user=request.user
            category_id=data.get('categoryId')
            specs=data.get('specs')
            category = ProductCategory.objects.get(id=int(category_id))
            try:
                product_specs = ProductsSpecification.objects.get(productCategory=category)
                product_specs.updated_by = user
                product_specs.updated_at = dt.now()
            except ProductsSpecification.DoesNotExist:
                product_specs = ProductsSpecification()
                product_specs.created_by = user
            product_specs.specs = specs
            product_specs.productCategory = category
            product_specs.save()
            return Response({
                'success':True,
                'message': 'Product category specification saved successfully.'
            },  status=status.HTTP_200_OK)
        except Exception,e:
            return Response({
                'success': False,
                'message': str(e)
            },  status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response()

    def put(self, request, *args, **kwargs):
        return Response()