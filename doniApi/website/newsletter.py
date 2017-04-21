from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import NewsLetter


class NewsLetterAPI(GenericAPIView):

    def post(self, request, *args, **kwargs):
        print request.DATA
        return Response({'success': True})

    def get(self, request, *args, **kwargs):
        return Response()