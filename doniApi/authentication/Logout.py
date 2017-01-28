from doniApi.apiImports import Response, GenericAPIView, status
from django.contrib.auth.views import logout


class LogOutAPI(GenericAPIView):

        def post(self, request, *args, **kwargs):
            logout(request, *args, **kwargs)
            return Response({'success': True}, status=status.HTTP_200_OK)