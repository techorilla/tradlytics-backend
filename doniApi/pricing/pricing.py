from doniApi.apiImports import Response, GenericAPIView, status
from doniGroup.authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import PriceMarket, ProductItemPrice, ProductItem
from django.db import IntegrityError
from datetime import datetime as dt
import dateutil.parser


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
        price_time = data.get('priceTime')
        comments = data.get('comments')
        price_items = data.get('priceItems')
        product_item = ProductItem.objects.get(id=product_item_id)
        price_market = PriceMarket.objects.get(id=price_market_id)
        if update_id:
            prod_price_item = ProductItemPrice.objects.get(id=update_id)
            msg = self.messages['successPUT']
            prod_price_item.update_by = user
            prod_price_item.update_at = dt.now()
        else:
            prod_price_item = ProductItemPrice()
            msg = self.messages['successPOST']
            prod_price_item.created_by = user

        prod_price_item.comments = comments
        prod_price_item.price_items = price_items
        prod_price_item.product_item = product_item
        prod_price_item.price_market = price_market
        prod_price_item.price_time = dateutil.parser.parse(price_time)
        prod_price_item.save()
        return Response({'success': True, 'message': msg}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.save_product_item_price(request.data, request.user)

    def get(self,  request, *args, **kwargs):
        queryset = ProductItemPrice.objects.all()

        return Response({

        })

    def put(self, request, *args, **kwargs):
        return self.save_product_item_price(request.data, request.user)

    def delete(self, request, *args, **kwargs):
        product_price_item_id = request.data.get('id')
        prod_price_item = ProductItemPrice.objects.get(id=product_price_item_id)
        prod_price_item.delete()
        return Response({'success': True, 'message': self.messages['successDELETE']}, status=status.HTTP_200_OK)


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


class WebsitePricingAPI(GenericAPIView):

    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, *args, **kwargs):
        data = {
            0: {
                'data': [
                    [1267401600000, 29.02],
                    [1267488000000, 90.46],
                    [1267574400000, 28.46],
                    [1267660800000, 8.63],
                    [1267747200000, 28.59],
                    [1268006400000, 28.63],
                    [1268092800000, 2.80],
                    [1268179200000, 28.97],
                    [1268265600000, 129.18],
                    [1268352000000, 3.27],
                    [1268611200000, 29.29],
                    [1268697600000, 229.37],
                    [1268784000000, 9.63],
                    [1268870400000, 29.61],
                    [1268956800000, 249.59],
                    [1269216000000, 29.60],
                    [1269302400000, 29.88],
                    [1269388800000, 59.65],
                    [1269475200000, 30.01],
                    [1269561600000, 9.66],
                    [1269820800000, 29.59],
                    [1269907200000, 29.77],
                    [1269993600000, 19.29]

                ],
                'name': 'Number 2 or better, Australia'
            }
        }
        return Response({'chartData': data})

    def post(self, request, *args, **kwargs):
        return Response()

    def delete(self, request, *args, **kwargs):
        return Response()

    def put(self, request, *args, **kwargs):
        return Response()