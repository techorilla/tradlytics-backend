from doniApi.apiImports import Response, GenericAPIView, status
from doniGroup.authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import *
from datetime import datetime as dt, timedelta
from django.db.models import Max
from django.db.models import Sum


class WebsitePricingGraphAPI(GenericAPIView):

    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, *args, **kwargs):
        product_item_id = int(kwargs.get('product_item_id'))
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_2 = start_date
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        graph_data = []
        product_item = ProductItem.objects.get(id=product_item_id)
        product = product_item.product_origin.product

        all_manifest_product_id = list()
        all_manifest_product_id.append(int(product.id))
        all_manifest_product_id = all_manifest_product_id + product.related_product_ids

        while start_date <= end_date:
            graph_item = dict()
            graph_item['date'] = start_date.strftime('%Y-%m-%d')
            try:
                local_price = product_item.price_product_item.filter(
                    price_time__startswith=start_date.date(),
                    price_market__origin='PK').order_by('-price_time')[0]
                graph_item['localPkrPkg'] = local_price.rs_per_kg
                graph_item['localUsdPmt'] = local_price.usd_per_pmt
            except IndexError:
                graph_item['localPkrPkg'] = None
                graph_item['localUsdPmt'] = None
                pass
            try:
                int_price =  product_item.price_product_item.filter(
                    price_time__startswith=start_date.date(),
                    price_market__origin='INT').order_by('-price_time')[0]
                graph_item['intPkrPkg'] = int_price.rs_per_kg
                graph_item['intUsdPmt'] = int_price.usd_per_pmt
            except IndexError:
                graph_item['intPkrPkg'] = None
                graph_item['intUsdPmt'] = None

            # Manifest Data
            try:
                import_volume = ManifestItem.objects.filter(product__id__in=all_manifest_product_id)\
                    .filter(date__startswith=start_date.date())\
                    .aggregate(Sum('quantity'))
                graph_item['importVolume'] = import_volume.get('quantity__sum')
            except Exception, e:
                print e
                pass


            graph_data.append(graph_item)
            start_date = start_date + timedelta(days=1)

        total_import = ManifestItem.objects.filter(product__id__in=all_manifest_product_id) \
            .filter(date__lte=end_date).filter(date__gte=start_date_2) \
            .aggregate(Sum('quantity'))


        ProductItemPrice.objects.filter(product_item__id=product_item_id).filter()


        return Response({
            'totalImport': total_import.get('quantity__sum'),
            'graphData': graph_data
        }, status=status.HTTP_200_OK)

