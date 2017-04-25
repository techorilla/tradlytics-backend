from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from doniServer.models import Products, ProductCategory, ProductItem, PriceSummary
from django.db.models import Max
from datetime import datetime as dt
from datetime import timedelta


class PricingPage(View):
    template_name = 'pricing.html'

    def get(self, request, *args, **kwargs):

        all_product_on_website = ProductItem.objects.filter(price_on_website=True).distinct()\
            .order_by('product_origin__product__name')

        price_summary = []

        for item in all_product_on_website:
            price_summary.append(item.price_market_summary)

        context = {
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