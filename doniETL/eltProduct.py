import requests
from .etlManager import *
from doniServer.models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class EtlProduct(EtlManager):
    GET_ALL_PRODUCT_URL = 'http://54.191.252.114:44200/getAllproducts'
    SINGLE_PRODUCT_URL = 'http://54.191.252.114:44200/getProduct/'
    MODEL = Products

    @staticmethod
    def get_all_product_id():
        data = requests.get(url=EtlProduct.GET_ALL_PRODUCT_URL, headers=EtlManager.HEADERS)
        all_products = data.json()
        return [product.get('id') for product in all_products]

    @staticmethod
    def get_single_product(product_id):
        data = requests.get(url=EtlProduct.SINGLE_PRODUCT_URL+str(product_id), headers=EtlManager.HEADERS)
        data = data.json()
        product = data.get('product')
        return product

    @staticmethod
    def get_all_product_complete_detail():
        all_product_id = EtlProduct.get_all_product_id()
        all_product_data = map(EtlProduct.get_single_product, all_product_id)
        return all_product_data

    def migrate_products(self):
        self.MODEL.objects.all().delete()
        ProductKeyword.objects.all().delete()
        all_products = EtlProduct.get_all_product_complete_detail()
        for product in all_products:
            EtlProduct.store_product_in_database(product)

    @staticmethod
    def store_product_in_database(product):
        created_by = User.objects.get(email='immadimtiaz@gmail.com')
        origin = Origin.get_origin_by_name(product.get('origin'))
        id = product.get('id')
        name = product.get('name')
        moisture = product.get('specs').get('moisture')
        wrinkled = product.get('specs').get('wrinkled')
        weeviled = product.get('specs').get('weeviled')
        splits = product.get('specs').get('splits')
        purity = product.get('specs').get('purity')
        other_color = product.get('specs').get('otherColor')
        foreign_matter = product.get('specs').get('foreignMatter')
        damaged = product.get('specs').get('damaged')
        green_damaged = product.get('specs').get('greedDamaged')
        quality = product.get('quality')
        quality = quality.split(',')
        product = Products.objects.create(id=id, name=name, moisture=moisture, purity=purity, weaveled=weeviled,
                                          origin=origin, splits=splits, damaged=damaged,
                                          foreignMatter=foreign_matter, greenDamaged=green_damaged,
                                          otherColor=other_color, wrinkled=wrinkled,
                                          created_at=timezone.now(), created_by=created_by, updated_at=None, )
        for q in quality:
            quality_keyword = q.strip()
            try:
                keyword = ProductKeyword.objects.get(keyword=quality_keyword)
                product.quality_keywords.add(keyword)
                product.save()
            except ProductKeyword.DoesNotExist:
                keyword = ProductKeyword.objects.create(keyword=quality_keyword, created_at=timezone.now(),
                                                        created_by=created_by, updated_at=None,)
                product.quality_keywords.add(keyword)
                product.save()











