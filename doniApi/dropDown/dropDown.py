from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.dropDowns import *
from doniInventory.models import Warehouse
from doniServer.models.product import ProductCategory, Products, PriceMarket, ProductKeyword, ProductItem, PriceMetric
from doniServer.models.product.priceMarket import get_all_currencies
from doniServer.models.shipment import ShippingPort, ShippingLine, Vessel
from doniServer.models import BpBasic, Transaction
from django.utils import timezone
from django.conf import settings
from doniCore import Utilities
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
import dateutil.parser
from doniCore import cache_results


class SimpleDropDownAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        business = Utilities.get_user_business(user)
        q = request.GET.get('q')
        if q == 'all' or q == 'drop_down':
            result_objects = self.model.objects.filter(created_by__profile__business=business)
            if q == 'all':
                results = [res.get_list_obj() for res in result_objects]
            else:
                results = [res.drop_down_obj() for res in result_objects]
            return Response({'list': results}, status=status.HTTP_200_OK)
        else:
            result_object = self.model.objects.get(id=int(q))
            return Response({'object': result_object.get_list_obj()}, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        try:
            user = request.user
            id = request.data.get('id')
            name = request.data.get('name')
            drop_down_obj = self.model.objects.get(id=id)
            drop_down_obj.name = name
            drop_down_obj.updated_by = user
            drop_down_obj.updated_at = timezone.now()
            drop_down_obj.save()
            return Response({
                'success': True,
                'message': 'Dropdown value updated successfully',
                'obj': drop_down_obj.get_list_obj()
            }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:

            user = request.user
            name = request.data.get('name')
            drop_down_obj = self.model.objects.create(
                name=name,
                created_at=timezone.now(),
                created_by=user,
                updated_at=None
            )
            return Response({
                'success': True,
                'message': 'Drop down value added successfully',
                'obj': drop_down_obj.get_list_obj()
            }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e),
            }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        id = request.data.get('id')
        drop_down_obj = self.model.objects.get(id=id)
        drop_down_obj.delete()
        return Response({'id': id}, status=status.HTTP_200_OK)


class BusinessDropDownAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    # @cache_results
    def get_all_business_drop_down(self, type, page, business_id):
        if not str(page):
            return BpBasic.get_drop_down_obj(type)
        else:
            return Transaction.get_business_type_drop_down_for_transaction_page(type, business_id)

    def get(self, request, *args, **kwargs):
        type = request.GET.get('type')
        page = request.GET.get('page')
        user = request.user
        all_business = self.get_all_business_drop_down(type, page, user.profile.business_id)
        return Response({
            'list': all_business
        }, status=status.HTTP_200_OK)


class CountryAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @cache_results
    def get_all_countries(self, tab_filter=False):
        from django_countries import countries
        not_entered = [{
            'name': 'Not Entered',
            'code': 'NotEntered',
        }]
        all_countries = list(countries)
        all_countries = [{
                             'name': c[1],
                             'code': c[0],
                             'image': settings.COUNTRIES_FLAG_URL.replace('{code}', str(c[0].lower()))
                         } for c in all_countries]
        return all_countries if not tab_filter else all_countries+not_entered

    def get(self, request, *args, **kwargs):
        tab_filter = request.GET.get('tabFilter')
        return Response({'list': self.get_all_countries(tab_filter)}, status=status.HTTP_200_OK)


class RegionAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        country_code = request.GET.get('q')
        from cities_light.models import Region
        regions = Region.objects.filter(country__code2=country_code).order_by('name')
        regions = [{
                       'id': region.name_ascii,
                       'name': region.name_ascii
                   } for region in regions]
        return Response({'list': regions}, status=status.HTTP_200_OK)


class CityAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        query = request.GET
        country_code = query.get('countryCode')
        region = query.get('region')
        from cities_light.models import City
        if not region:
            cities = City.objects.filter(country__code2=country_code).filter().order_by('name_ascii')
        else:
            cities = City.objects.filter(country__code2=country_code).filter(region__name_ascii=region).order_by('name_ascii')
        cities = [
            {
                'id': city.name_ascii,
                'name': city.name_ascii
            } for city in cities
        ]
        return Response({'list': cities}, status=status.HTTP_200_OK)


class ProductDDAPI(GenericAPIView):
    model = Products
    permission_classes = (IsAuthenticated,)

    @cache_results
    def get_product_drop_down(self):
        return self.model.get_dropdown()

    def get(self, request, *args, **kwrgs):
        return Response({'list': self.get_product_drop_down()}, status=status.HTTP_200_OK)


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

class CommissionTypeAPI(SimpleDropDownAPI):
    model = CommissionType

class PackagingAPI(SimpleDropDownAPI):
    model = Packaging

class BusinessTypeAPI(SimpleDropDownAPI):
    model = BusinessType


class ContactType(SimpleDropDownAPI):
    model = ContactType


class ContractType(SimpleDropDownAPI):
    model = TransactionContractType


class WarehouseDDAPI(SimpleDropDownAPI):
    model = Warehouse


class Designation(SimpleDropDownAPI):
    model = Designation


class PriceMetricDDAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        metrics = PriceMetric.objects.all().order_by('metric')
        metrics = [met.get_drop_down() for met in metrics]
        return Response({'list': metrics}, status=status.HTTP_200_OK)


class ProductKeywords(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    model = ProductKeyword

    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('q')
        if product_id != 'all':
            product = Products.objects.get(id=product_id)
            keywords = ProductKeyword.objects.filter(category=product.category)
        else:
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
        price_date = request.GET.get('q')
        if price_date != 'all':
            date = dateutil.parser.parse(price_date)
        else:
            date = dt.now()
        current_month = str(date.year)+'-'+str(date.month)+'-1'
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



class ShippingLineDDAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        all_line = ShippingLine.objects.all()
        all_line = [line.get_drop_down_obj() for line in all_line]
        return Response({'list': all_line}, status=status.HTTP_200_OK)


class ShippingVesselDDAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        all_vessel = Vessel.objects.all()
        all_vessel = [vessel.get_drop_down_obj() for vessel in all_vessel]
        return Response({
            'list': all_vessel
        }, status=status.HTTP_200_OK)


class ShippingPortDDAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        all_ports = ShippingPort.objects.all()
        all_ports = [port.get_drop_down_obj() for port in all_ports]
        return Response({
            'list': all_ports
        }, status=status.HTTP_200_OK)












