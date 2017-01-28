from doniApi.apiImports import Response, BaseAPI, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniCore import Utilities
from doniServer.models.authentication import UserProfile
from doniServer.models.businessPartner.bpLocations import BpLocation
from doniServer.models.dropDowns.designation import Designation
from doniCore.utils import Utilities
import os, sys


class UserProfilePicAPI(GenericAPIView):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        base_url = request.META.get('HTTP_HOST')
        user_id = kwargs.get('user_id')
        pic = request.FILES.get('profile')
        user_profile = UserProfile.objects.get(user__id=user_id)
        if user_profile.profile_pic:
            path = Utilities.get_media_directory()+'/'+str(user_profile.profile_pic)
            os.remove(path)
        user_profile.profile_pic = pic
        user_profile.save()
        return Response({'userId': user_id, 'profile_pic': user_profile.get_profile_pic(base_url)}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


class User(GenericAPIView, BaseAPI):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        q = request.GET.get('q')
        base_url = request.META.get('HTTP_HOST')
        business = Utilities.get_user_business(user)
        if q == self.ALL_QUERY or q == self.DROP_DOWN_QUERY:
            all_users = UserProfile.objects.filter(business=business)
            return Response({'list': [user.get_list_obj(request.user.id) for user in all_users]},
                            status=status.HTTP_200_OK)
        else:
            profile = UserProfile.objects.get(user__id=int(q))
            return Response({'user': profile.complete_profile(base_url)}, status=status.HTTP_200_OK)

    @staticmethod
    def set_profile_obj_from_request(profile, updated_user):
        business_loc_id = updated_user.get('businessLocationId')
        designation_id = updated_user.get('designationId')
        if business_loc_id:
            profile.businessLocation = BpLocation.objects.get(address_id=business_loc_id)
        if designation_id:
            profile.designation = Designation.objects.get(id=designation_id)
        notification = updated_user.get('notify')
        profile.notify_new_transaction = notification.get('newTransaction')
        profile.notify_shipment_arrival = notification.get('shipmentArrival')
        profile.notify_messages = notification.get('messages')
        profile.notify_monthly_reports = notification.get('monthlyReports')
        profile.notify_weekly_reports = notification.get('weeklyReports')
        profile.notify_daily_reports = notification.get('dailyReports')
        profile.save()

    def put(self, request, *args, **kwargs):
        updated_user = request.data.get('user')
        profile = UserProfile.objects.get(user__id=updated_user.get('id'))
        self.set_profile_obj_from_request(profile, updated_user)
        return Response({
            'user_id': updated_user.get('id'),
            'message': 'User profile Updated successfully'
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        return Response()

    def delete(self, request, *args, **kwargs):
        user = request.user
        return Response()