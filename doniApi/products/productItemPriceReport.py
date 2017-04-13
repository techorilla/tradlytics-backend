from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import ProductItemPrice, ProductItem
import pandas as pd
import dateutil.parser
from datetime import timedelta

class ProductItemPriceReportAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        start_date = request.GET.get(u'startDate')
        end_date = request.GET.get(u'endDate')
        product_item_id = request.GET.get(u'productItemId')
        start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
        end_date = dateutil.parser.parse(str(end_date).replace('"', ''))
        days_in_between = (end_date - start_date).days
        before_date = start_date - timedelta(days=days_in_between)
        product_item = ProductItem.objects.get(id=product_item_id)
        price_items = product_item.price_product_item.filter(price_time__lte=end_date, price_time__gte=before_date)
        price_items = [item.get_shipment_period_current_value for item in price_items]
        price_items_df = pd.DataFrame(price_items)
        price_items_df['price'] = price_items_df['price'].astype(float)
        markets = price_items_df['market'].unique()
        markets_price = dict()

        for market in markets:
            markets_price[market] = dict()
            market_df = price_items_df[price_items_df['market']== market]
            markets_price[market]['afterDataFrame'] = market_df[market_df['price_time'] >= start_date]
            markets_price[market]['beforeDataFrame'] = market_df[market_df['price_time'] < start_date]
            markets_price[market]['averagePrice'] = markets_price[market]['afterDataFrame']['price'].mean()
            if not markets_price[market]['beforeDataFrame'].empty:
                before_avg_price = markets_price[market]['beforeDataFrame']['price'].mean()
                avg_difference = float(markets_price[market]['averagePrice'])-float(before_avg_price)
                avg_per_change = (avg_difference/before_avg_price)*100
                markets_price[market]['beforeAveragePrice'] = before_avg_price
                markets_price[market]['averagePriceChange'] = avg_per_change
                markets_price[market]['difference'] = avg_difference
            markets_price[market][market + '_price'] = markets_price[market][market+'_price']

        print markets_price

        return Response({
            'success': True
        }, status=status.HTTP_200_OK)
