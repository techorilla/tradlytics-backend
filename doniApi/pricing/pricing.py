from doniApi.apiImports import Response, GenericAPIView, status
from doniGroup.authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import PriceMarket, ProductItemPrice, ProductItem, PriceMetric, PriceSummary
from django.db import IntegrityError
from datetime import datetime as dt
import dateutil.parser
from django.db.models import Max


class PricingSummaryAPI(GenericAPIView):
    permission_class = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        last_summary_date = PriceSummary.objects.all().aggregate(Max('summary_on'))
        last_summary_date = last_summary_date.get('summary_on__max')
        price_summary = PriceSummary.objects.filter(summary_on=last_summary_date)\
            .order_by('product_item__product_origin__product__name')

        return Response({
            'data':
                {
                    'priceSummary': [price.summary for price in price_summary]
                }
        }, status=status.HTTP_200_OK)


class ProductItemPricingAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    messages = dict()
    messages['successPOST'] = 'Product item price added successfully.'
    messages['successPUT'] = 'Product item price updated successfully.'
    messages['successDELETE'] = 'Product item price delete successfully.'

    def save_product_item_price(self, data, user):
        update_id = data.get('id')
        product_item_id = data.get('productItemId')
        price_market_id = data.get('priceMarketId')
        price_metric_metric = data.get('priceMetricId')
        price_time = data.get('priceTime')
        comments = data.get('comments')
        price_items = data.get('priceItems')
        product_item = ProductItem.objects.get(id=product_item_id)
        price_market = PriceMarket.objects.get(id=price_market_id)
        price_metric = PriceMetric.objects.get(metric=price_metric_metric)
        if update_id:
            prod_price_item = ProductItemPrice.objects.get(id=update_id)
            msg = self.messages['successPUT']
            prod_price_item.update_by = user
            prod_price_item.update_at = dt.now()
        else:
            prod_price_item = ProductItemPrice()
            msg = self.messages['successPOST']
            prod_price_item.created_by = user

        prod_price_item.price_metric = price_metric
        prod_price_item.comments = comments
        prod_price_item.price_items = price_items
        prod_price_item.product_item = product_item
        prod_price_item.price_market = price_market
        prod_price_item.price_time = dateutil.parser.parse(price_time)
        prod_price_item.save()
        PriceSummary.get_price_summary_for_product(product_item)
        return Response({'success': True, 'message': msg, 'obj': prod_price_item.get_obj()}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.save_product_item_price(request.data, request.user)

    def get(self,  request, *args, **kwargs):
        start_date = request.GET.get(u'startDate')
        end_date = request.GET.get(u'endDate')
        start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
        end_date = dateutil.parser.parse(str(end_date).replace('"', ''))
        queryset = ProductItemPrice.get_all_prices(start_date, end_date, request.user)
        return Response({
            'data': {'allPrices': queryset}
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return self.save_product_item_price(request.data, request.user)

    def delete(self, request, *args, **kwargs):
        try:
            product_price_item_id = kwargs.get('product_item_price_id')
            prod_price_item = ProductItemPrice.objects.get(id=product_price_item_id)
            prod_price_item.delete()
            return Response({'success': True, 'message': self.messages['successDELETE']}, status=status.HTTP_200_OK)
        except Exception,e:
            return Response({'success': False, 'message': str(e)})




class PricingMarketAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    international_origin = ('INT', 'International')

    def save_price_market(self, data, user, market=None, is_update=False):
        is_international = data.get('isInternational')

        if is_update:
            market = market
            market.updated_by = user
        else:
            market = PriceMarket()
            market.created_by = user

        if is_international:
            market.origin = 'INT'
        else:
            market.origin = data.get('country')

        market.currency = data.get('currency')
        market.description = data.get('description')
        try:
            market.save()
            return Response({'success': True, 'obj': market.get_obj()}, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({'success': False, 'message': 'This price market already exist'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        print request.data
        return self.save_price_market(data, user)

    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        market_id = data.get('id')
        market = PriceMarket.objects.get(id=market_id)
        return self.save_price_market(data, user, market=market, is_update=True)

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        pricing_market = PriceMarket.objects.all().order_by('origin')
        pricing_market = [market.get_obj() for market in pricing_market]
        return Response({'data': {'pricingMarket': pricing_market}}, status=status.HTTP_200_OK )

    def delete(self, request, *args, **kwargs):
        return Response({'success': True}, status=status.HTTP_200_OK)


