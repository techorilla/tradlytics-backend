import requests
from .etlManager import *
from doniServer.models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class EtlBusinessPartner(EtlManager):
    GET_ALL_BUSINESS_PARTNER_URL = 'http://54.191.252.114:44200/getBusinessPartnerList'
    SINGLE_BUSINESS_PARTNER_URL = 'http://54.191.252.114:44200/getBusinessPartnerFull/'
    MODEL = BpBasic

    @staticmethod
    def get_all_business_partner_ids():
        data = requests.get(url=EtlBusinessPartner.GET_ALL_BUSINESS_PARTNER_URL, headers=EtlManager.HEADERS)
        all_business_partner = data.json().get('data')
        return sorted([bp.get('bp_ID') for bp in all_business_partner])

    @staticmethod
    def get_complete_business_partner_details(bp_id):
        data = requests.get(url=EtlBusinessPartner.SINGLE_BUSINESS_PARTNER_URL+str(bp_id), headers=EtlManager.HEADERS)
        return data.json()

    @staticmethod
    def store_business_partner_in_db(bp_id):
        created_by = User.objects.get(email='immadimtiaz@gmail.com')
        bp_complete = EtlBusinessPartner.get_complete_business_partner_details(bp_id)
        products = bp_complete.get('products', [])
        emails = bp_complete.get('emails', [])
        contact_persons = bp_complete.get('contPers', [])
        contact_numbers = bp_complete.get('contNum',[])
        basic = bp_complete.get('gen')[0]
        banks = bp_complete.get('bank', [])

        # Storing Business Partner Basic Info
        bp_id = basic.get('bp_ID')
        name = (basic.get('bp_Name')).encode('utf-8')
        address = (basic.get('bp_address')).encode('utf-8')
        country = basic.get('bp_country')
        cred_index = basic.get('bp_credibilityIndex')
        is_broker = basic.get('bp_isBuyer')
        is_seller = basic.get('bp_isSeller')
        is_shipper = basic.get('bp_isShipper')
        is_buyer = basic.get('bp_isBuyer')
        website = basic.get('bp_website')
        doni_contract = basic.get('bp_onDoniContract')

        bp = BpBasic(bp_id=bp_id, bp_name=name, bp_website=website,  bp_credibility_index=cred_index,
                     bp_country=country, bp_address=address, bp_on_contract=doni_contract,
                     created_at=timezone.now(), created_by=created_by, updated_at=None)
        bp.save()

        if is_broker:
            broker = BpType.objects.get(type='Broker')
            bp.bp_types.add(broker)
        if is_buyer:
            buyer = BpType.objects.get(type='Buyer')
            bp.bp_types.add(buyer)
        if is_seller:
            seller = BpType.objects.get(type='Seller')
            bp.bp_types.add(seller)
        if is_shipper:
            shipper = BpType.objects.get(type='Shipper')
            bp.bp_types.add(shipper)

        bp.save()

        # Storing Business Partner Products
        for prod in products:
            product_id = prod.get('prod_ID')
            bp_product = Products.objects.get(id=product_id)
            BpProducts.objects.create(bp=bp, product=bp_product, created_at=timezone.now(),
                                      created_by=created_by, updated_at=None)

        # Storing Business Partner Contact Persons
        for contact in contact_persons:
            contact_id = contact.get('bp_cont_ID')
            cont_email = contact.get('bp_Cont_Email')
            cont_primary = contact.get('bp_Cont_IsPrimary')
            cont_primary_num = contact.get('bp_Cont_PrimaryNumber')
            cont_sec_num = contact.get('bp_Cont_SecondryNumber')
            cont_designation = contact.get('bp_Cont_designation')
            bp_cont_fullname = contact.get('bp_Cont_fullName')
            BpContact.objects.create(bp=bp, id=contact_id, is_primary=cont_primary, full_name=bp_cont_fullname,
                                     email=cont_email, primary_number=cont_primary_num, secondary_number=cont_sec_num,
                                     designation=cont_designation, created_at=timezone.now(), created_by=created_by,
                                     updated_at=None)

        # Storing Business Partner Banks
        for bank in banks:
            bank_country = bank.get('accountCountry')
            bank_id = bank.get('bankDetails_ID')
            bank_name = bank.get('bankName')
            account_title = bank.get('accountTitle')
            account_number = bank.get('accountNumber')
            bank_info = bank.get('branchAddress')
            BpBank.objects.create(bp=bp, acc_id=bank_id, bank_name=bank_name, branch_address=bank_info,
                                  acc_number=account_number, acc_title=account_title, acc_country=bank_country,
                                  created_at=timezone.now(), created_by=created_by, updated_at=None)

        # Storing Business Partner Contact Numbers
        for contact in contact_numbers:
            contact_type = contact.get('contactType')
            contact_number = contact.get('contactNumber')
            BpContactNumber.objects.create(bp=bp, contact_number=contact_number, type=contact_type, created_at=timezone.now(),
                                           created_by=created_by, updated_at=None)

    def migrate_business_partner(self):
        created_by = User.objects.get(email='immadimtiaz@gmail.com')
        BpType.objects.all().delete()
        BpBank.objects.all().delete()
        BpProducts.objects.all().delete()
        BpContact.objects.all().delete()
        BpContactNumber.objects.all().delete()
        BpEmail.objects.all().delete()
        self.MODEL.objects.all().delete()
        BpType.objects.create(type_id='1', type='Broker', created_by=created_by)
        BpType.objects.create(type_id='2', type='Seller', created_by=created_by)
        BpType.objects.create(type_id='3', type='Shipper', created_by=created_by)
        BpType.objects.create(type_id='4', type='Buyer', created_by=created_by)
        all_bp_ids = EtlBusinessPartner.get_all_business_partner_ids()
        map(EtlBusinessPartner.store_business_partner_in_db, all_bp_ids)




