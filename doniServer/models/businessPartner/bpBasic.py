from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone
from ..dropDowns.bptype import BusinessType
from django.conf import settings
from django.db import connection
import os
import time


def get_image_path(instance, filename):
    return os.path.join('businessLogo', instance.bp_name, str(time.time())+'_'+filename)


class BpBasic(models.Model):
    bp_id = models.AutoField(primary_key=True)
    bp_logo = models.ImageField(
        upload_to=get_image_path, blank=True, null=True)
    bp_name = models.CharField(max_length=255, blank=False)
    bp_ntn = models.CharField(max_length=30, blank=True)
    bp_website = models.CharField(max_length=255, null=False, blank=False)
    bp_credibility_index = models.IntegerField(default=1)
    bp_types = models.ManyToManyField(BusinessType, related_name='business')
    bp_database_id = models.CharField(max_length=5, null=True)
    bp_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_basic_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='bp_basic_updated_by')


    class Meta:
        db_table = 'bp_basic'

    def __unicode__(self):
        return self.bp_name.replace(' ', '_')

    @property
    def is_delete_able(self):
        manifest_items = self.buyer.count()
        trade_book_items = self.tr_basic_buyer.count()
        if manifest_items or trade_book_items:
            return False
        else:
            return True


    def get_business_logo(self, base_url):
        if settings.IS_HTTPS:
            pre = 'https://'
        else:
            pre = 'http://'
        return pre+base_url+'/media/'+str(self.bp_logo) if self.bp_logo else None


    @property
    def primary_contact(self):
        try:
            contact_person = self.contact_persons.get(is_primary=True)
            contact_person_name = contact_person.full_name
        except Exception, e:
            contact_person_name = None
        return contact_person_name

    @property
    def primary_state(self):
        try:
            primary_location = self.locations.get(is_primary=True)
            state = primary_location.state
            return state
        except Exception, e:
            return None

    @property
    def primary_city(self):
        try:
            primary_location = self.locations.get(is_primary=True)
            city = primary_location.city
            return city
        except Exception, e:
            return None

    @property
    def primary_origin(self):
        try:
            primary_location = self.locations.get(is_primary=True)
            primary_country_code = primary_location.country
            from django_countries import countries
            primary_country = dict(countries)[primary_country_code]
            primary_country_flag = settings.COUNTRIES_FLAG_URL.replace('{code}', str(primary_country_code.lower()))
        except Exception, e:
            primary_country_code = None
            primary_country = None
            primary_country_flag = None
        return primary_country, primary_country_code, primary_country_flag


    @classmethod
    def get_drop_down_obj(cls, business_type):
        cur = connection.cursor()
        cur.callproc('business_drop_down_list', [business_type, ])
        field_names = [i[0] for i in cur.description]
        all_business = cur.fetchall()
        cur.close()
        return [dict(zip(field_names, item)) for item in all_business]

    def get_list_obj(self, base_url):
        bp_types_id, bp_type_str = self.get_by_types_names()
        try:
            contact_person = self.contact_persons.get(is_primary=True)
            contact_person_name = contact_person.full_name
        except Exception, e:
            contact_person_name = None

        try:
            primary_location = self.locations.get(is_primary=True)
            primary_country_code = primary_location.country
            from django_countries import countries
            primary_country = dict(countries)[primary_country_code]

        except Exception, e:
            primary_country_code = None
            primary_country = None



        return {
            'bpId': self.bp_id,
            'logo': self.get_logo(base_url),
            'name': self.bp_name,
            'website': self.bp_website,
            'ntn': self.bp_ntn,
            'bpTypeId': bp_types_id,
            'bpTypeStr': bp_type_str,
            'contactPerson': contact_person_name,
            'countryCode': primary_country_code if primary_country else 'NotEntered',
            'country': primary_country if primary_country else 'Not Entered'
        }

    def get_by_type_id(self):
        bp_types = self.bp_types.all().order_by('name')
        bp_types = [type.id for type in bp_types]
        return bp_types

    def get_by_types_names(self):
        bp_types = self.bp_types.all().order_by('name')
        bp_types = [{
                        'id': typ.id,
                        'name': typ.name
                    } for typ in bp_types]
        bp_types_names = [typ.get('name') for typ in bp_types]
        bp_types_id = [typ.get('id') for typ in bp_types]
        bp_types_names = ', '.join(bp_types_names)
        return bp_types_id, bp_types_names

    def get_obj(self, base_url):
        locations = self.locations.all()
        contact_persons = self.contact_persons.all()
        contact_persons = [cont_person.get_obj() for cont_person in contact_persons]
        locations = [loc.get_obj() for loc in locations]
        contacts = self.contacts.all()
        contacts = [cont.get_obj() for cont in contacts]
        banks = self.banks.all()
        banks = [bank.get_obj() for bank in banks]
        return {
            'bpId': self.bp_id,
            'logo': self.get_logo(base_url),
            'name': self.bp_name,
            'website': self.bp_website,
            'ntn': self.bp_ntn,
            'bpType': self.get_by_type_id(),
            'databaseId': self.bp_database_id,
            'banks': banks,
            'locations': locations,
            'contacts': contacts,
            'contactPersons': contact_persons
        }


    def get_logo(self, base_url):
        if settings.IS_HTTPS:
            pre = 'https://'
        else:
            pre = 'http://'
        return pre + base_url + '/media/' + str(self.bp_logo) if self.bp_logo else None

    @classmethod
    def get_admin_business(cls):
        business_admin = cls.objects.get(bp_admin=True)
        return business_admin

    @classmethod
    def get_business_using_website(cls, url):
        business = cls.objects.get(bp_website__contains=url)
        return business


    def get_description_obj(self, base_url):
        country, country_code, country_flag = self.primary_origin
        return {
            'id': self.bp_id,
            'name': self.bp_name,
            'country': country,
            'website': self.bp_website,
            'countryFlag': country_flag,
            'primaryContact': self.primary_contact,
            'logo': None if not self.bp_logo else self.get_business_logo(base_url)
        }


