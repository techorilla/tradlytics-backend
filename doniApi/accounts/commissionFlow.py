from doniApi.apiImports import Response, GenericAPIView, status


class CommissionFlowAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        print request.GET
        return Response({
            'invoiceObj':{}
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response()

    def delete(self, request, *args, **kwargs):
        return Response()

    def put(self, request, *args, **kwargs):
        return Response()
