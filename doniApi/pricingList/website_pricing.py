from doniApi.apiImports import Response, GenericAPIView, status
from doniGroup.authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import *
from datetime import datetime as dt, timedelta
from django.db.models import Max
from django.db.models import Sum

def get_product_pricing_data(product_item, all_manifest_product_id, start_date, end_date):
    counter_date = start_date
    graph_data = []
    while counter_date <= end_date:
        graph_item = dict()
        graph_item['date'] = counter_date.strftime('%Y-%m-%d')
        try:
            local_price = product_item.price_product_item.filter(
                price_time__startswith=counter_date.date(),
                price_market__origin='PK').order_by('-price_time')[0]
            graph_item['localPkrPkg'] = local_price.rs_per_kg
            graph_item['localUsdPmt'] = local_price.usd_per_pmt
        except IndexError:
            graph_item['localPkrPkg'] = None
            graph_item['localUsdPmt'] = None
            pass
        try:
            int_price = product_item.price_product_item.filter(
                price_time__startswith=counter_date.date(),
                price_market__origin='INT').order_by('-price_time')[0]
            graph_item['intPkrPkg'] = int_price.rs_per_kg
            graph_item['intUsdPmt'] = int_price.usd_per_pmt
        except IndexError:
            graph_item['intPkrPkg'] = None
            graph_item['intUsdPmt'] = None

        # Manifest Data
        try:
            import_volume = ManifestItem.objects.filter(product__id__in=all_manifest_product_id) \
                .filter(date__startswith=counter_date.date()) \
                .aggregate(Sum('quantity'))
            graph_item['importVolume'] = import_volume.get('quantity__sum')
        except Exception, e:
            pass

        graph_data.append(graph_item)
        counter_date = counter_date + timedelta(days=1)

    ## Manifest Query Set
    all_manifest_query_set = ManifestItem.objects.filter(product__id__in=all_manifest_product_id) \
        .filter(date__lte=end_date).filter(date__gte=start_date)
    total_import = all_manifest_query_set.aggregate(Sum('quantity'))
    total_import = total_import.get('quantity__sum')

    return graph_data, total_import


class WebsitePricingGraphAPI(GenericAPIView):

    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, *args, **kwargs):
        date_limit = '2017-04-01'
        product_item_id = int(kwargs.get('product_item_id'))
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        start_date = dt.strptime(start_date, '%Y-%m-%d') if not (str(start_date) < date_limit) else  dt.strptime(date_limit, '%Y-%m-%d')
        start_date_2 = start_date
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        # graph_data = []
        product_item = ProductItem.objects.get(id=product_item_id)
        all_manifest_product_id = product_item.get_related_product_ids()
        graph_data, total_import = get_product_pricing_data(product_item, all_manifest_product_id,start_date,end_date)


        all_manifest_query_set = ManifestItem.objects.filter(product__id__in=all_manifest_product_id) \
            .filter(date__lte=end_date).filter(date__gte=start_date_2)



        ## Pakistan Market Import Volume Distribution

        state_import = dict()
        city_import = dict()

        for item in all_manifest_query_set:


            if item.buyer.primary_state not in state_import.keys():
                state_import[item.buyer.primary_state] = 0
            state_import[item.buyer.primary_state] = state_import[item.buyer.primary_state] + item.quantity

            if item.buyer.primary_city not in city_import.keys():
                city_import[item.buyer.primary_city] = {
                    'state': item.buyer.primary_state,
                    'quantity': 0
                }
            city_import[item.buyer.primary_city]['quantity'] = city_import[item.buyer.primary_city]['quantity'] + item.quantity

        city_import_data = []
        for key, data in city_import.items():
            data.update({'city': key})
            city_import_data.append(data)


        return Response({
            'volumeSummary': {
                'stateImport': [{'state': imports[0], 'import': imports[1]} for imports in state_import.items()],
                'cityImport': city_import_data
            },
            'totalImport': total_import,
            'graphData': graph_data
        }, status=status.HTTP_200_OK)

