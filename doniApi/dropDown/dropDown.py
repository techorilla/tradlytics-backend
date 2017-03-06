from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.dropDowns import *
from doniServer.models.product import ProductCategory, Products, PriceMarket, ProductKeyword, ProductItem
from doniServer.models.product.priceMarket import get_all_currencies
from django.utils import timezone
from django.conf import settings
from doniCore import Utilities
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta


class SimpleDropDownAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        business = Utilities.get_user_business(user)
        q = request.GET.get('q')
        if q == 'all' or q == 'drop_down':
            result_objects = self.model.objects.filter(business=business)
            if q == 'all':
                results = [res.get_list_obj() for res in result_objects]
            else:
                results = [res.drop_down_obj() for res in result_objects]
            return Response({'list': results}, status=status.HTTP_200_OK)
        else:
            result_object = self.model.objects.get(id=int(q))
            return Response({'object': result_object.get_list_obj()}, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        user = request.user
        id = request.data.get('id')
        name = request.data.get('name')
        drop_down_obj = self.model.objects.get(id=id)
        drop_down_obj.name = name
        drop_down_obj.updated_by = user
        drop_down_obj.updated_at = timezone.now()
        drop_down_obj.save()
        return Response({'obj': drop_down_obj.get_list_obj()}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        business = Utilities.get_user_business(user)
        name = request.data.get('name')
        drop_down_obj = self.model.objects.create(
            name=name,
            created_at=timezone.now(),
            created_by=user,
            updated_at=None,
            business=business
        )
        return Response({'obj': drop_down_obj.get_list_obj()}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        id = request.data.get('id')
        drop_down_obj = self.model.objects.get(id=id)
        drop_down_obj.delete()
        return Response({'id': id}, status=status.HTTP_200_OK)


class CountryAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        from django_countries import countries
        all_countries = list(countries)
        all_countries = [{
                             'ticked': False,
                             'name': c[1],
                             'code': c[0],
                             'image': settings.COUNTRIES_FLAG_URL.replace('{code}', str(c[0].lower()))
                         } for c in all_countries]
        return Response({'list': all_countries}, status=status.HTTP_200_OK)



class ProductDDAPI(GenericAPIView):
    model = Products
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwrgs):
        return Response({'list': self.model.get_dropdown()}, status=status.HTTP_200_OK)


class ProductOriginDDAPI(GenericAPIView):
    model = Products
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('q')
        product = self.model.objects.get(id=product_id)
        origins = product.origins
        origins = [{
                        'name': org.country.name,
                        'code': org.country.code,
                        'image': settings.COUNTRIES_FLAG_URL.replace('{code}', str(org.country.code.lower()))
                   } for org in origins]
        return Response({'list': origins}, status=status.HTTP_200_OK)


class ProductCategoryDDAPI(GenericAPIView):
    model = ProductCategory
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({'list': self.model.get_category_drop_down()}, status=status.HTTP_200_OK)


class PriceMarketDDAPI(GenericAPIView):
    model = PriceMarket
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response()


class CurrencyDDAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        currencies = get_all_currencies()
        currencies = [{
            'code': currency[0],
            'name': currency[1]
        } for currency in currencies]
        return Response({'list': currencies}, status=status.HTTP_200_OK)


class BusinessTypeAPI(SimpleDropDownAPI):
    model = BusinessType


class ContactType(SimpleDropDownAPI):
    model = ContactType


class ContractType(SimpleDropDownAPI):
    model = TransactionContractType


class Designation(SimpleDropDownAPI):
    model = Designation


class ProductKeywords(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    model = ProductKeyword

    def get(self, request, *args, **kwargs):
        keywords = ProductKeyword.objects.all()
        keywords = [key.get_obj() for key in keywords]
        return Response({'list': keywords},  status=status.HTTP_200_OK)


class PriceMarketDDAPI(GenericAPIView):

    def get(self, request, *args, **kwargs):
        price_market = PriceMarket.objects.all().order_by('origin')
        price_market = [market.get_dropdown() for market in price_market]
        return Response({'list': price_market}, status=status.HTTP_200_OK)

class ProductItemDDAPI(GenericAPIView):

    def get(self, request, *args, **kwargs):
        product_items = ProductItem.objects.all().order_by('product_origin__product__name')
        product_items = [product.get_dropdown() for product in product_items]
        return Response({'list': product_items}, status=status.HTTP_200_OK)


class ShipmentMonthDDAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        today = dt.now()
        current_month = str(today.year)+'-'+str(today.month)+'-1'
        start_month = dt.strptime(current_month, '%Y-%m-%d')
        price_span_months = 12
        shipment_months = []
        for month in range(price_span_months):
            ship_month = start_month + relativedelta(months=month)
            shipment_months.append(ship_month)

        shipment_months = [{
            'startMonth': month,
            'month': month.strftime("%B"),
            'year': month.year
        } for month in shipment_months]

        return Response({'list': shipment_months}, status=status.HTTP_200_OK)


class TransactionStatus(SimpleDropDownAPI):
    model = TransactionStatus








