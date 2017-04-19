from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from doniServer.models import Products, ProductCategory, ProductItem, PriceSummary
from django.db.models import Max
from datetime import datetime as dt
from datetime import timedelta


class PricingPage(View):
    template_name = 'pricing.html'

    def get(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        last_summary_date = PriceSummary.objects.all().aggregate(Max('summary_on'))
        last_summary_date = last_summary_date.get('summary_on__max')
        price_summary = PriceSummary.objects.filter(summary_on=last_summary_date) \
            .order_by('product_item__product_origin__product__name')
        all_products = Products.objects.all()

        context = {
            'allProducts': all_products,
            'priceSummary': price_summary
        }
        return render(request, self.template_name, context)


class PricingDetail(View):
    template_name = 'pricing_details.html'

    def get(self, request, *args, **kwargs):
        now = dt.now()
        year_ago = now - timedelta(days=365)

        product_id = query = request.GET.get("id")
        base_url = request.META.get('HTTP_HOST')
        product_item = ProductItem.objects.get(id=product_id)
        context = {
            'productItem': product_item
        }
        return render(request, self.template_name, context)