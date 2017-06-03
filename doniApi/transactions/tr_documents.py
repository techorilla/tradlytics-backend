from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import TrFiles, Transaction

class TransactionDocumentAPI(GenericAPIView):

    def get(self, request, *args, **kwargs):
        print 'hello'
        return Response()

    def post(self, request, *args, **kwargs):
        data =  request.data
        trade_id = data.get(u'tradeId')[0]
        extension = data.get(u'extension')[0]
        filename = data.get(u'name')[0]
        document = request.FILES.get('file')
        transaction = Transaction.objects.get(tr_id=trade_id)

        tr_file = TrFiles()
        tr_file.file = document
        tr_file.file_name = filename
        tr_file.extension = extension
        tr_file.transaction = transaction
        tr_file.save()


        return Response({
            'success':True
        })

    def delete(self, request, *args, **kwargs):
        return Response()

    def put(self, request, *args, **kwargs):
        return Response()