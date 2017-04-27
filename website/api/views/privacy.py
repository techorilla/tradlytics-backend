from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from doniServer.models import Products, ProductCategory, ProductItem, PriceSummary
from django.db.models import Max
from datetime import datetime as dt
from datetime import timedelta

class PrivacyPage(View):
    template_name = 'privacy.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)