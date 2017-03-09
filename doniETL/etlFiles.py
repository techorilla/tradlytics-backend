import pandas as pd
from doniServer.models import *
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
import numpy as np

file_path = '~/rates/international.xlsx'
local_path = '~/rates/local.xlsx'
sheet_name = 'International Rate'
sheet_name_locat = 'Local Rate'

international_market = PriceMarket.objects.get(id=1)
local_market = PriceMarket.objects.get(id=2)

priceItemObject = [
    {
        'shipmentMonths': [],
        'priceValue': '',
        'currentValue': True
    }
]

crimson_lentils = ProductItem.objects.get(id=14)
kabuli_indian = ProductItem.objects.get(id=17)
desi_chick = ProductItem.objects.get(id=10)
yellow_peas = ProductItem.objects.get(id=19)
blank_mapte = ProductItem.objects.get(id=4)
created_by = User.objects.get(username='immadimtiaz')
columns_name = ['date', '14', '17', '10', '19', '4']


products = [
    u'Date',
    u'Red Lentils Crimson Canada',
    u'Kabuli CP Indian 9mm',
    u'Desi chick Peas Aust',
    u'Yellow Peas Russ/Ukr',
    u'Black Mapte SQ Burma'
]

product_2 = [
    u'Date',
    u'Red Lentils Crimson',
    u'Kabuli CP Indian 9mm',
    u'Desi chick Peas Local',
    u'Yellow Peas Russ/Ukr',
    u'Black Mapte SQ'
]

def read_excel_file(filePath, sheetName):
    file = pd.ExcelFile(filePath)
    return file.parse(sheetName, convert_float=False)

def transfer_international_prices(file_path, sheet_name):
    dataframe = read_excel_file(file_path, sheet_name)
    dataframe = dataframe[products]
    dataframe.columns = columns_name
    dataframe = dataframe.set_index('date', drop=True)
    def save_product_price(row):
        product_item_id = row.index
        for id in product_item_id:
            if not np.isnan(row[id]):
                product_item = ProductItem.objects.get(id=id)
                shipment_months = get_shipment_months(row.name, 1)
                price_items = [
                    {
                        'shipmentMonths': shipment_months,
                        'priceValue': '%.2f' % (row[id]),
                        'currentValue': True
                    }
                ]
                save_price_item_price(product_item, international_market, row.name, price_items, created_by)

                # print product_item.product_origin.product.name, price_items, row.name, row[id], price_items
        return True
    dataframe.apply(save_product_price, axis=1)
    return dataframe

def transfer_local_price(file_path, sheet_name):
    dataframe = read_excel_file(file_path, sheet_name)
    dataframe = dataframe[product_2]
    dataframe.columns = columns_name
    dataframe = dataframe.set_index('date', drop=True)
    def save_product_price(row):
        product_item_id = row.index
        for id in product_item_id:
            try:
                if not np.isnan(row[id]):
                    product_item = ProductItem.objects.get(id=id)
                    shipment_months = get_shipment_months(row.name, 1)
                    price_items = [
                        {
                            'shipmentMonths': shipment_months,
                            'priceValue': '%.2f' % (row[id]),
                            'currentValue': True
                        }
                    ]
                    save_price_item_price(product_item, local_market, row.name, price_items, created_by)
            except TypeError:
                pass
        return True
    dataframe.apply(save_product_price, axis=1)
    return dataframe



def save_price_item_price(product_item, price_market, price_time, price_items, created_by):
    item_price = ProductItemPrice()
    item_price.product_item = product_item
    item_price.price_market = price_market
    item_price.price_time = price_time
    item_price.price_items = price_items
    item_price.created_by = created_by
    item_price.save()


def get_shipment_months(date, month_diff):
    price_month = str(date.year) + '-' + str(date.month) + '-1'
    price_month = dt.strptime(price_month, '%Y-%m-%d')
    shipment_month = price_month + relativedelta(months=1)
    return [price_month.strftime('%Y-%m-%d')+'T00:00:00', shipment_month.strftime('%Y-%m-%d')+'T00:00:00']






