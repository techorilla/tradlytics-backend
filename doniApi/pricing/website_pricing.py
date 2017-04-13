from doniApi.apiImports import Response, GenericAPIView, status
from doniGroup.authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import *



class WebsitePricingAPI(GenericAPIView):

    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, *args, **kwargs):

        product_items = ProductItem.objects.all()
        product_items = [item for item in product_items]
        international_price = [item.get_price_website('INT') for item in product_items]
        international_price = [item for item in international_price if item is not None]
        local_price = [item.get_price_website('PKT') for item in product_items]
        local_price = [item for item in local_price if item is not None]
        return Response({
            'internationalPrice': international_price,
            'localPrice': local_price
        }, status=status.HTTP_200_OK)

