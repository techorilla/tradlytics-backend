from django.contrib.auth.models import User
from django.db import models
from ..businessPartner.bpBasic import BpBasic
from ..dropDowns.designation import Designation
from ..dropDowns.contactType import ContactType
from doniServer.models.businessPartner.bpLocations import BpLocation
from django.utils import timezone
from django.conf import settings
import time
import os


def get_image_path(instance, filename):
    return os.path.join('profilePic', instance.business.bp_name, instance.user.username, str(time.time())+'_'+filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    small_profile_pic = models.ImageField(
        upload_to=get_image_path, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to=get_image_path, blank=True, null=True)
    business = models.OneToOneField(BpBasic)
    notify_new_transaction = models.BooleanField(default=False)
    notify_shipment_arrival = models.BooleanField(default=False)
    notify_messages = models.BooleanField(default=False)
    notify_monthly_reports = models.BooleanField(default=True)
    notify_weekly_reports = models.BooleanField(default=True)
    notify_daily_reports = models.BooleanField(default=True)
    designation = models.ForeignKey(Designation, null=True)
    businessLocation = models.ForeignKey(BpLocation, null=True)

    class Meta:
        db_table = 'user_profile'

    def get_profile_pic(self, base_url):
        if settings.IS_HTTPS:
            pre = 'https://'
        else:
            pre = 'http://'
        return pre+base_url+'/media/'+str(self.profile_pic) if self.small_profile_pic else None

    def complete_profile(self, base_url):
        return {
            'id': self.user.id,
            'profilePic': self.get_profile_pic(base_url),
            'username': self.user.username,
            'firstName': self.user.first_name,
            'lastName': self.user.last_name,
            'email': self.user.email,
            'designationId': self.designation.id if self.designation else None,
            'businessLocationId': self.businessLocation.address_id if self.businessLocation else None,
            'notify': {
                'newTransaction': self.notify_new_transaction,
                'shipmentArrival': self.notify_shipment_arrival,
                'messages': self.notify_messages,
                'monthlyReports': self.notify_monthly_reports,
                'weeklyReports': self.notify_weekly_reports,
                'dailyReports': self.notify_daily_reports
            }
        }

    def get_list_obj(self, user_id):
        return {
            'id': self.user.id,
            'userName': self.user.username,
            'lastName': self.user.last_name,
            'firstName': self.user.first_name,
            'active': self.user.is_active,
            'isStaff': self.user.is_staff,
            'lastLogin': self.user.last_login,
            'email': self.user.email,
            'designation': self.designation.name,
            'self': (self.user.id == user_id)
        }


class UserContactNumbers(models.Model):
    user = models.ForeignKey(User)
    country_code = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=100)
    contact_type = models.ForeignKey(ContactType)
    extension = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='user_contact_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='user_contact_updated_by')
    business = models.ForeignKey(BpBasic, null=True)

    class Meta:
        db_table = 'user_contact_number'



