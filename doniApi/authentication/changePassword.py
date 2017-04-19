from doniApi.apiImports import Response, APIView, status, AllowAny
from django.contrib.auth import authenticate, login
from doniServer.models import UserSession
from django.contrib.auth.models import *


class ChangePassword(APIView):

    def post(self, request, *args, **kwargs):
        params = request.data

        def error_response(error):
            return Response({
                'success': error,
                'message': 'Incorrect Password'
            },  status=status.HTTP_200_OK)

        if request.user.is_authenticated():
            print request.user
            password = params.get('oldPassword')
            user = authenticate(username=request.user.username,
                                password=password,
                                dashboard=True)
            if not user:
                return error_response('Incorrect Password')
            new_password = params.get('newPassword')
            confirm_password = params.get('confirmPassword')
            print new_password, confirm_password
            if new_password and new_password == confirm_password:
                try:
                    user = User.objects.get(username=request.user.username)
                    user.set_password(new_password)
                    user.save()
                    return Response({
                        'success': True,
                        'message': 'User Password Changed successfully'
                    }, status=status.HTTP_200_OK)
                except Exception, e:
                    return error_response(str(e))