import pandas as pd
from doniServer.models import *
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
import numpy as np
from cities_light.models import City, Region, Country
from django.conf import settings
import dateutil.parser
from doniServer.models.shipment import Vessel

vessel_imo_file_path = settings.PROJECT_ROOT + '/dataSheets/imo-vessel-codes.csv'
manifest_file_path = settings.PROJECT_ROOT + '/dataSheets/manifest.xlsx'
shipper_file_path = settings.PROJECT_ROOT + '/dataSheets/shippingLines.xlsx'
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


metric_fcl = PriceMetric.objects.get(metric='FCL')
metric_kgs = PriceMetric.objects.get(metric='KG')
metric_40_kgs = PriceMetric.objects.get(metric='40 KG')


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

def get_vessel_imo_numbers():
    not_exist = []
    vessel_type_of_interest = ['Container Ship', 'Bulk Carrier', 'General Cargo', 'Cargo/Container Ship']
    def update_mmsi_number(row):
        imo_number = row['imo']
        mmsi_number = row['mmsi']
        type = row['type']
        name = row['name']
        try:
            vessel=Vessel.objects.get(imo_number=imo_number)
            vessel.mmsi_number = mmsi_number
            vessel.save()
        except Vessel.DoesNotExist:
            not_exist.append(imo_number)
            if type in vessel_type_of_interest:
                vessel= Vessel()
                vessel.imo_number = imo_number
                vessel.mmsi_number = mmsi_number
                vessel.name = name
                vessel.first_name = name
                vessel.created_by = created_by
                vessel.save()
                print 'Vessel Does not Exist %s'%imo_number
    df = pd.read_csv(vessel_imo_file_path )
    df.apply(update_mmsi_number, axis=1)
    return not_exist


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
                save_price_item_price(product_item, international_market, row.name, price_items, metric_fcl, created_by)

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
                    if product_item == blank_mapte:
                        metric = metric_40_kgs
                    else:
                        metric = metric_kgs
                    shipment_months = get_shipment_months(row.name, 1)
                    price_items = [
                        {
                            'shipmentMonths': shipment_months,
                            'priceValue': '%.2f' % (row[id]),
                            'currentValue': True
                        }
                    ]
                    save_price_item_price(product_item, local_market, row.name, price_items, metric, created_by)
            except TypeError:
                pass
        return True
    dataframe.apply(save_product_price, axis=1)
    return dataframe


def save_price_item_price(product_item, price_market, price_time, price_items, price_metric, created_by):
    item_price = ProductItemPrice()
    item_price.product_item = product_item
    item_price.price_market = price_market
    item_price.price_time = price_time
    item_price.price_items = price_items
    item_price.created_by = created_by
    item_price.price_metric = price_metric
    item_price.save()


def get_shipment_months(date, month_diff):
    price_month = str(date.year) + '-' + str(date.month) + '-1'
    price_month = dt.strptime(price_month, '%Y-%m-%d')
    shipment_month = price_month + relativedelta(months=1)
    return [price_month.strftime('%Y-%m-%d')+'T00:00:00', shipment_month.strftime('%Y-%m-%d')+'T00:00:00']

all_product = {
        'Agriculture Beans': [
            u'Black Matpe',
            u'Black Eyed Beans',
            u'Bamboo Beans',
            u'Broad Beans',
            u'Brown Eye Beans',
            u'Canela Beans',
            u'Cow Peas Beans',
            u'Cranberry Beans',
            u'Green Mung Beans',
            u'Light Red Kidney Beans',
            u'Light Speckled Kidney Beans',
            u'Red Speckled Kidney Beans',
            u'Red Kidney Beans',
            u'Pinto Beans',
            u'Garbanzo Beans',
            u'Purple Speckled Kidney Beans',
            u'Yellow Soya Beans',
            u'Dark Red Kidney Beans',
            u'Whole Bean',
            u'Soybean',
        ],
        'Agriculture Bran': [
            u'Bran Channa',
            u'Bran Lentil',
            u'Bran Masoor',
            u'Wheat Bran',
            u'Yellow Peas Bran',
        ],
        'Agriculture Seeds': [
            u'Berseem Clover Seeds',
            u'Coriander Seeds',
            u'Safflower Seeds',
            u'Sea Bean Seed',
            u'Corn Seed',
            u'Caraway Seeds',
            u'Planting Seeds',
            u'Sorghum Seeds',
            u'Rapeseed',
            u'Canary Seed',
            u'Bean Seeds',
        ],
        'Agriculture Oil Seeds':[
            u'RBD Palm Olein',
            u'Canola Seeds',
            u'Sunflower Seed',
            u'Palm Kernel',
            u'Canola',
            u'Safflower'
        ],
        'Agriculture Husk': [
            u'Husk',
            u'Pigeon Peas Husk',

        ],
        'Agriculture Peas': [
            u'Sultan Peas',
            u'Peas',
            u'Pigeon Peas',
            u'Yellow Peas',
            u'Kabuli Chick Peas',
            u'Desi Chick Peas',
            u'Dun Peas Kaspa',
            u'Field Peas',
            u'Green Peas'
        ],
        'Agriculture Lentils':[
            u'Crimson Lentils / Nipper Nugget',
            u'Blaze Lentils',
            u'Eston Lentils',
            u'Red Lentils',
            u'Flash lentils',
            u'Green Lentils',
            u'Richlea Lentils',
            u'Laird Lentils',
            u'Impala Lentils',

        ],
        'Agriculture Processed': [
            u'Bean Powder',
            u'Soybean Meal',
            u'Wheat Flour',
            u'Vital Wheat Gluten',
            u'Pop Corn',
            u'Milk Powder',
            u'Sugar'
        ],
        'Agriculture Millet': [
            u'Green Millet',
            u'Grey Millet',
            u'Millet',
            u'Indian Millet',
            u'Yellow Sorghum Millet',
            u'Sorghum'
        ],
        'Agriculture Grains': [
            u'Oats',
            u'Wheat',
            u'Corn / Maize',
            u'Barley'
        ],
        'Animal Feed': [
            u'Beans For Animal Feed',
            u'Cattle Feed'
        ],
        'Agriculture Groundnuts':[
            u'Peanut',
            u'Peanut Kernel'
        ]
    }


def create_all_products():
    for (category, products) in all_product.items():
        cat = ProductCategory.objects.get(name=category)
        for prod in products:
            try:
                product = Products.objects.get(name=prod)
                print 'Exist ' + prod
            except Products.DoesNotExist:
                product = Products()
                product.name = prod
                product.category = cat
                product.created_by = created_by
                product.save()
                print 'Does Not Exist ' + prod


def transfer_all_manifest_items():
    metric = PriceMetric.objects.get(metric='FCL')
    dataFrame = read_excel_file(manifest_file_path, 'Manifest')
    df = dataFrame.copy()

    df = df[['Date', 'Seller', 'Buyer Name', 'Product', 'QTY (FCL)', 'Cont No']]
    for item in df.values:
        manifest_date = item[0]
        manifest_date = dateutil.parser.parse(str(manifest_date))
        seller_name = item[1]
        buyer_name = item[2]
        product_name = item[3]
        quantity = int(item[4])
        container_no = item[5]
        if pd.isnull(seller_name) == False:
            buyer = BpBasic.objects.get(bp_name=buyer_name, bp_types__name='Buyer')
            seller = BpBasic.objects.get(bp_name=seller_name, bp_types__name='Seller')
            product = Products.objects.get(name=product_name)
            manifest_item = ManifestItem()
            manifest_item.date = manifest_date
            manifest_item.quantity = quantity
            manifest_item.quantity_metric = metric
            manifest_item.buyer = buyer
            manifest_item.seller = seller
            manifest_item.product = product
            manifest_item.container_no = container_no
            manifest_item.created_by = created_by
            manifest_item.save()
            print manifest_date, buyer.bp_name, seller.bp_name, product.name, quantity
    return


def create_all_shippers():
    dataFrame = read_excel_file(shipper_file_path, 'Sheet1')
    df = dataFrame.copy()
    shipper_type = BusinessType.objects.get(name='Shipper')
    city_error=[]
    for shipper in df.values:
        name = shipper[0]
        website = shipper[1]
        seller_city = shipper[3]
        country = shipper[4]
        address = shipper[6]
        try:
            city = City.objects.get(name_ascii=seller_city)
        except City.MultipleObjectsReturned:
            city = City.objects.get(name_ascii=seller_city, country__name_ascii__contains=country)
        except Exception, e:
            if ',' in seller_city:
                city_region = seller_city.split(',')
                city = City.objects.get(name_ascii=city_region[0], region__name_ascii=city_region[1],
                                        country__name_ascii__contains=country)
            else:
                city_error.append(seller_city)
        business = BpBasic()
        location = BpLocation()
        business.bp_name = name
        business.bp_website = website
        business.created_by = created_by
        business.save()
        business.bp_types.add(shipper_type)
        business.save()
        location.bp = business
        location.is_primary = True
        location.city = city.name_ascii,
        location.state = city.region.name_ascii
        location.country = city.country.code2
        location.address = address
        location.created_by = created_by
        location.save()
    return city_error



def create_all_sellers():
    def create_seller(seller_name, seller_address, website, seller_city=None, seller_state=None):
        buyer_type = BusinessType.objects.get(name='Seller')
        business = BpBasic()
        location = BpLocation()

        if seller_city:
            city_name = city.name_ascii
            location.city = city_name
            state = city.region.name_ascii
            country = city.country.code2
            location.state = state
            location.country = country
        if seller_state:
            state = seller_state.name_ascii
            country = seller_state.country.code2
            location.state = state
            location.country = country
        business.bp_name = seller_name
        business.bp_website = website
        business.created_by = created_by
        business.save()
        business.bp_types.add(buyer_type)
        business.save()
        location.bp = business
        location.is_primary = True
        location.address = seller_address

        location.created_by = created_by
        location.save()
        return

    dataFrame = read_excel_file(manifest_file_path, 'Manifest')
    df = dataFrame.copy()
    all_sellers = df[['Seller', 'City/Region', 'Seller Address', 'Seller Website']]
    for seller in all_sellers.values:
        seller_name = seller[0]
        seller_city = seller[1]
        seller_address = seller[2]
        seller_website = seller[3]
        state = None
        try:
            city = City.objects.get(name_ascii=seller_city)
        except City.MultipleObjectsReturned:
            cities = City.objects.filter(name_ascii=seller_city)
            for city_item in cities:
                if city_item.region.name_ascii in seller_address:
                    city = city_item
                    break
                if city_item.country.name_ascii in seller_address:
                    city = city_item
                    break
        except City.DoesNotExist:
            city = None
            if ',' in seller_city:
                city_split = seller_city.split(',')
                state = Region.objects.get(name_ascii=city_split[0].strip(), country__name_ascii=city_split[1].strip())
        try:
            business = BpBasic.objects.get(bp_name=seller_name, bp_types__name='Seller')
        except BpBasic.DoesNotExist:
            create_seller(seller_name, seller_address, seller_website, seller_city=city, seller_state=state)
    return None


def create_all_buyers():
    def create_buyer(name, city, address):
        buyer_type = BusinessType.objects.get(name='Buyer')
        business = BpBasic()
        location = BpLocation()
        state = city.region.name_ascii
        country = city.country.code2
        city_name = city.name_ascii
        business.bp_name = name
        business.created_by = created_by
        business.save()
        business.bp_types.add(buyer_type)
        business.save()
        location.bp = business
        location.is_primary = True
        location.address = address
        location.city = city_name
        location.state = state
        location.country = country
        location.created_by = created_by
        location.save()
        return
    dataFrame = read_excel_file(manifest_file_path, 'Manifest')
    all_buyers = dataFrame[['Buyer Name', 'City', 'Buyer Address']]
    for buyer in all_buyers.values:
        buyer_name = buyer[0]
        buyer_city = buyer[1]
        try:
            city = City.objects.get(name_ascii=buyer_city)
        except City.MultipleObjectsReturned:
            city = City.objects.get(name_ascii=buyer_city, country__name='Pakistan')
        try:
            business = BpBasic.objects.get(bp_name=buyer_name)
            if city.name_ascii != business.primary_city:
                create_buyer(buyer_name, city, buyer_address)
            else:
                print 'Already Exist'
        except BpBasic.DoesNotExist:
            buyer_address = buyer[2]
            create_buyer(buyer_name, city, buyer_address)
    return 'All Buyers Created'



def check_all_products_in_manifest_exist():
    dataFrame = read_excel_file(manifest_file_path, 'Manifest')
    products = dataFrame['Product']
    products = products.unique()
    does_not_exist = []
    for prod in products:
        print prod
        try:
            Products.objects.get(name=prod)
        except Products.DoesNotExist:
            does_not_exist.append(prod)
    return does_not_exist


def get_unique_buyers():
    dataFrame = read_excel_file(manifest_file_path, 'Manifest')
    buyers_details = dataFrame[['Buyer Name', 'City']]










