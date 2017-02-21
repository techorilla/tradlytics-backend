from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from doniServer.models import Products, ProductCategory


class ProductPage(View):
    template_name = 'products.html'

    def get(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        all_products = Products.get_products_for_website(base_url)
        context = {
            'products': all_products,
            'categories': ProductCategory.get_category_for_website()
        }
        return render(request, self.template_name, context)


class SingleProductPage(View):
    template_name = 'single_product.html'

    def get(self, request, *args, **kwargs):
        product_id = query = request.GET.get("id")
        base_url = request.META.get('HTTP_HOST')
        product = Products.objects.get(id=product_id)
        context = {
            'product': product,
            'web_obj': product.get_product_single_website(base_url)
        }
        return render(request, self.template_name, context)
