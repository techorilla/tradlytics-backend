from doniApi.apiImports import Response, APIView, status, AllowAny
from django.contrib.auth import authenticate, login
from doniServer.models import UserSession
from django.contrib.auth.models import *


class ChangePassword(APIView):

    def post(self, request, *args, **kwargs):
        params = request.DATA if request.DATA else request.DATA
        if request.user.is_authenticated():
            password = params.get('current_password')
            user = authenticate(email=request.user.email,
                                password=password,
                                dashboard=True)
            if not user:
                return Response('error', status.HTTP_400_BAD_REQUEST)
            new_password = params.get('new_password')
            confirm_password = params.get('confirm_password')

            if new_password and new_password == confirm_password:
                try:
                    user = User.objects.get(username=request.user.username)
                    user.set_password(new_password)
                    user.save()
                    return Response('success')
                except:
                    return Response('error', status.HTTP_400_BAD_REQUEST)

        return Response('error', status.HTTP_400_BAD_REQUEST)