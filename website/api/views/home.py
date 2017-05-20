from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from website.models import HomeSlider, HomeServices
from doniServer.models import *
from datetime import datetime as dt, time

class HomePage(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):

        slides = HomeSlider.objects.all()
        services = HomeServices.objects.all()
        context = {
            'ticker_items': ProductItem.get_price_ticker(),
            'slides': slides,
            'services': services
        }
        return render(request, 'home.html', context)


