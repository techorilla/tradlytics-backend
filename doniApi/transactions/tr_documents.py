from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import TrFiles, Transaction
from rest_framework.permissions import IsAuthenticated, AllowAny
import base64, binascii
from django.http import HttpResponse


class TransactionDocumentAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        doc_id = kwargs.get('document_id')
        doc = TrFiles.objects.get(file_id=doc_id)
        binary_doc = doc.file

        content_disposition = 'attachment; filename="%s"'%doc.file_name
        content_type = 'application/%s' % doc.extension
        response = HttpResponse(str(binary_doc.decode('hex')), content_type='application/octet-stream')
        response['Content-Disposition'] = content_disposition
        return response

    def post(self, request, *args, **kwargs):
        data =  request.data
        trade_id = str(data.get(u'tradeId'))
        extension = data.get(u'extension')
        filename = data.get(u'name')
        document = request.FILES.get('file')
        doc_read = document.read()
        # print doc_64_encode
        transaction = Transaction.objects.get(tr_id=trade_id)

        tr_file = TrFiles()
        tr_file.file = doc_read
        tr_file.file_name = filename
        tr_file.extension = 'application/'+extension
        tr_file.transaction = transaction
        tr_file.created_by = request.user
        tr_file.save()


        return Response({
            'success':True,
            'fileObj': {
                'fileId': tr_file.file_id,
                'fileName': tr_file.file_name,
                'uploadedBy': tr_file.created_by.username,
                'uploadedAt': tr_file.created_at,
                'extension': tr_file.extension,
            }
        })

    def delete(self, request, *args, **kwargs):
        file_id = kwargs.get('document_id')
        document = TrFiles.objects.get(file_id=file_id)
        document_name = document.file_name
        transaction_file_id = document.transaction.file_id
        document.delete()
        return Response({
            'success': True,
            'message': 'Document %s for transaction with file no. %s deleted successfully.' % (document_name, transaction_file_id)
        })

    def put(self, request, *args, **kwargs):
        return Response()