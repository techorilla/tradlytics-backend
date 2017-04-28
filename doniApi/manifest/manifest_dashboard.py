from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.businessPartner.bpBank import BpBank, BpBasic
from doniServer.models.manifest import ManifestItem
from doniServer.models.product import Products, PriceMetric
from datetime import datetime as dt
import pandas as pd
import dateutil.parser


class ManifestDashboardAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        raise ValueError('A very specific bad thing happened')
        start_date = request.data.get(u'startDate')
        end_date = request.data.get(u'endDate')
        selectedBuyer = request.data.get(u'selectedBuyer')
        selectedSeller = request.data.get(u'selectedSeller')
        selectedProduct = request.data.get(u'selectedProduct')
        start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
        end_date = dateutil.parser.parse(str(end_date).replace('"', ''))
        manifest_items = ManifestItem.get_manifest_items(start_date, end_date)
        manifest_items_df = pd.DataFrame(manifest_items)

        if not manifest_items_df.empty:
            all_quantity = manifest_items_df['quantity']
            all_quantity_sum = all_quantity.sum()
        else:
            all_quantity_sum = 0


        if selectedBuyer and not manifest_items_df.empty:
            buyers_df = pd.DataFrame(selectedBuyer.split(','), columns=['buyerId'])
            buyers_df['buyerId'] = buyers_df['buyerId'].apply(pd.to_numeric)
            manifest_items_df = pd.merge(manifest_items_df, buyers_df, on='buyerId', how='inner')

        if selectedSeller and not manifest_items_df.empty:
            seller_df = pd.DataFrame(selectedSeller.split(','), columns=['sellerId'])
            seller_df['sellerId'] = seller_df['sellerId'].apply(pd.to_numeric)
            manifest_items_df = pd.merge(manifest_items_df, seller_df, on='sellerId', how='inner')

        if selectedProduct and not manifest_items_df.empty:
            product_df = pd.DataFrame(selectedProduct.split(','), columns=['productId'])
            product_df['productId'] = product_df['productId'].apply(pd.to_numeric)
            manifest_items_df = pd.merge(manifest_items_df, product_df, on='productId', how='inner')

        ## Filtered Quantity
        if not manifest_items_df.empty:
            filtered_quantity = manifest_items_df['quantity']
            filtered_quantity_sum = filtered_quantity.sum()
            try:
                sum_percentage = float(filtered_quantity_sum)/float(all_quantity_sum) if (filtered_quantity_sum != 0) else 0
                sum_percentage = sum_percentage*100
            except ZeroDivisionError:
                sum_percentage = 0
        else:
            filtered_quantity_sum = 0
            sum_percentage = 0

        ## prepare Graph data
        if not manifest_items_df.empty:
            graph_df = manifest_items_df.groupby(['date']).agg({'quantity': sum})
            graph_df.reset_index(level=0, inplace=True)
            graph_df = graph_df.T.to_dict().values()
        else:
            graph_df = []

        ## prepare Sum Data

        sum_data = dict()
        sum_data['total'] = all_quantity_sum
        sum_data['filteredSum'] = filtered_quantity_sum
        sum_data['sumPercentage'] = sum_percentage
        print sum_data
        return Response({
            'graphData': graph_df,
            'sumData': sum_data
        }, status=status.HTTP_200_OK)