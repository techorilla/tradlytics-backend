from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from website.models import HomeSlider
from doniServer.models import *

class HomePage(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        product_items = ProductItem.objects.filter(price_on_website=True)
        product_items = [item for item in product_items]
        international_price = [item.get_price_website('INT') for item in product_items]
        international_price = [item for item in international_price if item is not None]
        slides = HomeSlider.objects.all()
        context = {
            'prices': international_price,
            'slides': slides
        }
        return render(request, 'home.html', context)


