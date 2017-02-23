from django.contrib import admin
from django.contrib.admin import AdminSite
from doniServer.models import *


admin.site.register(ProductCategory, ProductsCategoryAdmin)
admin.site.register(Products, ProductAdmin)

admin.site.register(ProductKeyword, ProductKeywordAdmin)
admin.site.register(ProductsSpecification, ProductsSpecificationAdmin)
admin.site.register(PriceMarket, PriceMarketAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)
admin.site.register(ProductOrigin, ProductOriginAdmin)
