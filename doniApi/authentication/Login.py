from doniApi.apiImports import Response, APIView, status, AllowAny
from django.contrib.auth import authenticate, login
from doniServer.models import UserSession, UserProfile
from django.contrib.auth.models import User
from doniGroup.authentication import CsrfExemptSessionAuthentication
from doniCore import Utilities

class LoginAPI(APIView):

    permission_classes = (AllowAny,)

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def set_login(self, request, username, password):
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            UserSession.set_session_key(
                request.user, request.session.session_key)
            return True
        return False

    def get_user_details(self, username, base_url):
        user = User.objects.get(username=username)
        business = Utilities.get_user_business(user)
        profile = UserProfile.objects.get(user__id=user.id)
        return {
            'id': user.id,
            'username': user.username,
            'isStaff': user.is_staff,
            'isSuperuser': user.is_superuser,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'businessId': business.bp_id,
            'businessName': business.bp_name,
            'smallProfilePic':  profile.get_profile_pic(base_url)
        }

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous():
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        base_url = request.META.get('HTTP_HOST')
        return Response({'userData': self.get_user_details(user.username, base_url)}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        params = request.data
        username = params.get('username')
        base_url = request.META.get('HTTP_HOST')
        if username:
            password = params.get('password')
            if self.set_login(request, username, password):
                return Response({'userData': self.get_user_details(username, base_url)}, status=status.HTTP_200_OK)
        return Response('INVALID_CREDENTIALS', status=status.HTTP_404_NOT_FOUND)
