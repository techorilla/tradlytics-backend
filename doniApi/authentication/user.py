from doniApi.apiImports import Response, BaseAPI, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User as UserObj
from doniServer.models.authentication import UserProfile
from doniServer.models.businessPartner.bpLocations import BpLocation
from doniServer.models.dropDowns.designation import Designation
from doniCore.utils import Utilities
from datetime import datetime as dt
from django.db import IntegrityError

import os, sys


class UserProfilePicAPI(GenericAPIView):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        base_url = request.META.get('HTTP_HOST')
        user_id = kwargs.get('user_id')
        pic = request.FILES.get('profile')
        user_profile = UserProfile.objects.get(user__id=user_id)

        if user_profile.profile_pic:
            try:
                path = Utilities.get_media_directory()+'/'+str(user_profile.profile_pic)
                os.remove(path)
            except OSError:
                pass
        user_profile.profile_pic = pic
        user_profile.save()
        print user_profile.__dict__
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
    def set_profile_obj_from_request(updated_user, profile=None, business=None):
        business_loc_id = updated_user.get('businessLocationId')
        designation_id = updated_user.get('designationId')
        if profile is None:
            profile = UserProfile()
            profile.business = business
        if business_loc_id:
            profile.businessLocation = BpLocation.objects.get(address_id=business_loc_id)
        if designation_id:
            profile.designation = Designation.objects.get(id=designation_id)
        notification = updated_user.get('notify')
        rights = updated_user.get('rights')
        profile.notify_new_transaction = notification.get('newTransaction')
        profile.notify_shipment_arrival = notification.get('shipmentArrival')
        profile.notify_messages = notification.get('messages')
        profile.notify_monthly_reports = notification.get('monthlyReports', False)
        profile.notify_weekly_reports = notification.get('weeklyReports', False)
        profile.notify_daily_reports = notification.get('dailyReports', False)
        profile.right_business_analytics = rights.get('businessAnalytics', False)
        profile.right_user_management = rights.get('userManagement', False)
        profile.right_warehouse_module = rights.get('warehouseModule', False)
        profile.right_business_commission = rights.get('businessCommission', False)
        return profile

    @staticmethod
    def generate_default_password():
        return 'doniGroup'

    @classmethod
    def set_user_obj_from_request(cls, user_data, user=None):
        password = None
        if user is None:
            user = UserObj()
            user.is_staff = True
            user.is_superuser = False
            password = cls.generate_default_password()
        user.first_name = user_data.get('firstName')
        user.last_name = user_data.get('lastName')
        user.username = user_data.get('username')
        user.email = user_data.get('email')
        user.save()
        if password:
            user.set_password(password)
            user.save()
        return user

    def put(self, request, *args, **kwargs):
        updated_user = request.data.get('user')
        username = updated_user.get('username')
        user = UserObj.objects.get(username=username)
        self.set_user_obj_from_request(updated_user, user=user)
        profile = UserProfile.objects.get(user__id=updated_user.get('id'))
        profile = self.set_profile_obj_from_request(updated_user, profile=profile)
        profile.updated_by = request.user
        profile.updated_at = dt.now()
        profile.save()
        return Response({
            'success': True,
            'user_id': updated_user.get('id'),
            'message': 'User profile Updated successfully'
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            try:
                new_user_data = request.data.get('user')
                user = self.set_user_obj_from_request(new_user_data)
            except IntegrityError as e:
                if e[1] == "Duplicate entry '' for key 'username'":
                    return Response({
                        'success': False,
                        'message': 'A user with this user name already exist'
                    })
            except Exception, e:
                return Response({
                    'success': False,
                    'message': str(e)
                })

            business = Utilities.get_user_business(request.user)
            new_profile = self.set_profile_obj_from_request(new_user_data, business=business)
            new_profile.user = user
            new_profile.created_by = request.user
            new_profile.created_at = dt.now()
            new_profile.save()
            return Response({
                'success': True,
                'user_id': user.id,
                'message': 'User Profile Added Successfully'
            })
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })

    def delete(self, request, *args, **kwargs):
        user = request.user
        return Response()