from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import IntTradeInvoice, Transaction
from datetime import datetime as dt
import dateutil.parser


class InvoiceAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        invoice_id =  str(request.GET.get('invoiceId'))
        file_id = str(request.GET.get('fileId'))
        trade = Transaction.objects.get(file_id=file_id)

        if invoice_id=='new':
            invoice_obj = IntTradeInvoice.get_default_invoice_obj(base_url, trade)
        else:
            invoice = IntTradeInvoice.objects.get(invoice_no=invoice_id)
            invoice_obj = invoice.get_complete_obj(base_url)

        return Response({
            'invoiceObj':invoice_obj
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.save_invoice(request)

    def save_invoice(self, request):
        user = request.user
        data=request.data
        invoice_obj = data.get('invoiceObj')
        file_id = data.get('fileId')
        transaction = Transaction.objects.get(file_id=file_id)
        invoice_items = invoice_obj.get('invoiceItems')
        invoice_no = invoice_obj.get('invoiceNo')
        invoice_date = invoice_obj.get('date')
        invoice_note = invoice_obj.get('note')
        invoice_amount = invoice_obj.get('invoiceAmount')
        invoice_to_id = invoice_obj.get('invoiceTo', {}).get('id')


        invoice_quantity_fcl = invoice_obj.get('quantityFCL')
        invoice_currency_rate = invoice_obj.get('currencyRate')
        if invoice_date:
            invoice_date = dateutil.parser.parse(str(invoice_date).replace('"', ''))
            invoice_date = invoice_date.replace(hour=0, minute=0, second=0, microsecond=0)

        if IntTradeInvoice.objects.filter(invoice_no=invoice_no).exists():
            invoice = IntTradeInvoice.objects.filter(invoice_no=invoice_no)
            invoice.updated_by = user
            invoice.updated_at = dt.now()
            message = 'Invoice %s for File Id %s created successfully!'%(invoice_no, file_id)

        else:
            invoice = IntTradeInvoice()
            invoice.transaction = transaction
            invoice.created_by = user
            message = 'Invoice %s for File Id %s created successfully!' % (invoice_no, file_id)

        invoice.invoice_to_id = invoice_to_id
        invoice.invoice_no = invoice_no
        invoice.invoice_date = invoice_date
        invoice.invoice_amount = invoice_amount
        invoice.invoice_items = invoice_items
        invoice.currency_rate = invoice_currency_rate
        invoice.note = invoice_note
        if transaction.quantity_fcl != invoice_quantity_fcl:
            transaction.quantity_fcl = invoice_quantity_fcl
            transaction.updated_by = user
            transaction.updated_at = dt.now()
            transaction.save()
        invoice.save()
        return Response({
            'success':True,
            'message': message
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response()

    def put(self, request, *args, **kwargs):
        return self.save_invoice(request)
