from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.businessPartner.bpBank import BpBank, BpBasic
from doniServer.models.manifest import ManifestItem
from doniServer.models.product import Products, PriceMetric
from datetime import datetime as dt
import dateutil.parser


class ManifestAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        start_date = request.GET.get(u'startDate')
        end_date = request.GET.get(u'endDate')
        start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
        end_date = dateutil.parser.parse(str(end_date).replace('"', ''))

        return Response({
            'manifestItems': ManifestItem.get_manifest_items(start_date, end_date)
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            manifest_id = kwargs.get('manifest_id')
            manifest_item = ManifestItem.objects.get(id=manifest_id)
            manifest_item.delete()
            message = 'Manifest Item successfully deleted.'
            success = True
        except Exception, e:
            success = False
            message = str(e)
        return Response({
            'manifest_id': manifest_id,
            'success': success,
            'message': message
        }, status=status.HTTP_200_OK)

    def save_manifest_item(self, data, user):
        try:
            data = data.get('manifestItem')
            manifest_id = data.get('id')
            metric = data.get('quantityMetricId')
            manifest_date = dateutil.parser.parse(data.get('date'))
            buyer_id = data.get('buyerId')
            seller_id = data.get('sellerId')
            product_id = data.get('productId')
            quantity = data.get('quantity')
            container_no = data.get('containerNo')
            if int(buyer_id) == int(seller_id):
                return Response({
                    'success': False,
                    'message': 'Buyer and Supplier can not be same'
                }, status=status.HTTP_200_OK)
            if manifest_id:
                manifest_item = ManifestItem.objects.get(id=int(manifest_id))
                manifest_item.updated_by = user
                manifest_item.updated_at = dt.now()
                message = 'Manifest item updated successfully'
            else:
                manifest_item = ManifestItem()
                manifest_item.created_by = user
                message = 'Manifest item created successfully'
            manifest_item.date = manifest_date
            manifest_item.quantity = quantity
            manifest_item.quantity_metric = PriceMetric.objects.get(metric=metric)
            manifest_item.buyer = BpBasic.objects.get(bp_id=int(buyer_id))
            manifest_item.seller = BpBasic.objects.get(bp_id=int(seller_id))
            manifest_item.product = Products.objects.get(id=int(product_id))
            manifest_item.container_no = container_no
            manifest_item.save()
            return Response({
                'success': True,
                'message': message,
                'item': manifest_item.get_list_obj(),
            }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({'success': False, 'message': str(e)})

    def post(self, request, *args, **kwargs):
        return self.save_manifest_item(request.data, request.user)

    def put(self, request, *args, **kwargs):
        return self.save_manifest_item(request.data, request.user)
