from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import IntTradeInvoice, Transaction


class InvoiceAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        invoice_id =  str(request.GET.get('invoiceId'))
        file_id = str(request.GET.get('fileId'))
        trade = Transaction.objects.get(file_id=file_id)

        if invoice_id=='new':
            invoice_obj = IntTradeInvoice.get_default_invoice_obj(base_url, trade)

        return Response({
            'invoiceObj':invoice_obj
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response()

    def delete(self, request, *args, **kwargs):
        return Response()

    def put(self, request, *args, **kwargs):
        return Response()
