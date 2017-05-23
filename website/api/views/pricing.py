from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from doniServer.models import Products, ProductCategory, ProductItem, PriceSummary
from django.db.models import Max
from datetime import datetime as dt
from datetime import timedelta
from django.conf import settings


class PricingPage(View):
    template_name = 'pricing.html'

    def get(self, request, *args, **kwargs):

        all_product_on_website = ProductItem.objects.filter(price_on_website=True).distinct() \
            .order_by('price_on_website_order')

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
        order = product_item.price_on_website_order

        prod_list = ProductItem.objects.filter(price_on_website=True).exclude(id=product_id).distinct() \
            .order_by('price_on_website_order')








        context = {
            'productList': prod_list,
            'priceSummary': product_item.price_market_summary,
            'productItem': product_item,
            'productItemFlagURl': product_item.product_origin.country.flag
        }
        return render(request, self.template_name, context)