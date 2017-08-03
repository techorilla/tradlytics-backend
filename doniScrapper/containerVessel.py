from string import ascii_lowercase
from doniScrapper.proxy_manager import ProxyManager
from bs4 import BeautifulSoup
from doniServer.models import BpBasic, Transaction, BusinessAppProfile, TrShipment, TransactionShipmentTracking
from doniServer.models.shipment import Vessel, ShippingPort
from django.contrib.auth.models import User
import requests, time
import re
import dateutil.parser
from operator import itemgetter
from doniServer.celery import app

VESSEL_FINDER_URL = 'https://www.vesselfinder.com/vessels/%s-IMO-%s-MMSI-%s'

def get_port_by_containing_city_country(city, country):
    all_string = city.replace('(', ' ').replace(')', ' ').replace('  ', ' ').replace('PORT', '').strip().split(' ')
    all_string = list(set(all_string))
    for query in all_string:
        try:
            port = ShippingPort.objects.get(country__icontains=country.strip(), name__icontains=query)
            return {
                u'id': port.id,
                u'lo_code': port.lo_code,
                u'name': port.name,
                u'country': port.country
            }
        except ShippingPort.DoesNotExist:
            pass
    return None


@app.task
def get_vessel_position_for_all_business_app_profile():
    all_business_profiles = BusinessAppProfile.objects.all()
    for profile in all_business_profiles:
        business_not_shipped_info =  get_vessel_position_for_all_non_shipped(profile.business)
        business_not_shipped_info = [info for info in business_not_shipped_info if info is not None]
        tr = TransactionShipmentTracking()
        tr.business = profile.business
        tr.data = business_not_shipped_info
        tr.save()


def get_vessel_position_for_all_non_shipped(business):
    return get_vessel_position_transactions(Transaction.get_expected_arrival(business))

def get_vessel_position_transactions(transactions=[]):
    return map(get_vessel_position_for_transaction, transactions)

def save_transit_ports(vessel_position, transaction):
    destination = transaction.shipment.port_destination
    shipping_ports_found = vessel_position['lastFivePorts']
    shipping_ports_found = sorted(shipping_ports_found, key=itemgetter('date'), reverse=True)
    shipping_ports_found_mapping = []
    lo_code_added_already = []
    vessel_position['destinationReached'] = False
    for port in shipping_ports_found:
        arrival_date = port['date']
        mapping_found = get_port_by_containing_city_country(port['name'], port['country'])
        if mapping_found:
            mapping_found['date'] = arrival_date
            if mapping_found['lo_code'] == destination.lo_code:
                vessel_position['destinationReached'] = True
            if mapping_found['lo_code'] not in lo_code_added_already:
                shipping_ports_found_mapping.append(mapping_found)
                lo_code_added_already.append(mapping_found['lo_code'])
    shipping_ports_found_mapping = [port for port in shipping_ports_found_mapping if port is not None]
    shipping_ports_found_mapping = [dict(y) for y in set(tuple(x.items()) for x in shipping_ports_found_mapping)]
    transaction.shipment.transit_port =  shipping_ports_found_mapping
    transaction.shipment.save()

def get_vessel_position_for_transaction(transaction):
    if transaction.shipment.vessel:
        destination = transaction.shipment.port_destination
        vessel_position = get_vessel_position(transaction.shipment.vessel)
        vessel_position['fileId'] = transaction.file_id
        vessel_position['contractId'] = transaction.contract_id
        vessel_position['bl'] = transaction.shipment.bl_no
        vessel_position['vesselName'] = transaction.shipment.vessel.first_name
        vessel_position['containers'] = 0 if not transaction.shipment.containers else len(transaction.shipment.containers)
        vessel_position['portDestination'] = str(destination.name) + ', ' + str(transaction.shipment.port_destination.country)
        vessel_position['quantity'] = transaction.commission.quantity_shipped if transaction.commission.quantity_shipped else transaction.quantity
        seller_country = transaction.seller.primary_country
        vessel_position['seller'] = transaction.seller.bp_name if not seller_country else  transaction.seller.bp_name + ', ' + seller_country
        buyer_country = transaction.buyer.primary_country
        vessel_position['buyer'] = transaction.buyer.bp_name if not buyer_country else  transaction.buyer.bp_name + ', ' + buyer_country
        vessel_position['product'] = transaction.product_item.product_origin.product.name
        vessel_position['shippingLine'] = 'NA' if not transaction.shipment.shipping_line else transaction.shipment.shipping_line.name
        save_transit_ports(vessel_position, transaction)
        time.sleep(5)
        return vessel_position
    else:
        return None


def get_vessel_position(vessel):
    name = vessel.first_name if vessel.first_name else vessel.name
    name = name.upper().strip().replace(' ', '-')
    url = VESSEL_FINDER_URL%(name, vessel.imo_number, vessel.mmsi_number)
    response = requests.get(url, headers={'User-Agent': 'Google Chrome'})
    soup = BeautifulSoup(response.text, 'html.parser')
    longitude_element = soup.find("span", {'itemprop':'latitude'})
    latitude_element = soup.find("span", {'itemprop': 'longitude'})
    last_five_ports_elements = soup.find_all("div", {'itemtype':'http://schema.org/Event'})
    position_obj = dict()
    position_obj['longitude'] = longitude_element.text
    position_obj['latitude'] = latitude_element.text
    position_obj['lastFivePorts'] = []
    for port in last_five_ports_elements:
        last_port = dict()
        arrival_date = port.find('span', {'class': 'small-5 medium-6 columns'}).text
        city_country = port.find('a').text.split(',')
        last_port['name'] = city_country[0]
        last_port['country'] = city_country[1]
        last_port['date'] = dateutil.parser.parse(arrival_date)
        position_obj['lastFivePorts'].append(last_port)
    return position_obj




class VesselScrapper(object):

    URL = 'http://www.containership-info.com/%s'

    SHIPPING_COMPANY_NOT_FOUND = []

    VESSEL_COUNT = 0

    def get_all_vessels(self):
        all_vessels = []
        for c in ascii_lowercase:
            url = self.URL % 'page_names_'+c+'.html'
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            all_anchors = soup.find_all('a', href=re.compile(r'vessel_\S{7}'))
            for a in all_anchors:
                vessel_name = re.sub(r'\(.*\)', '', a.findChild().text.strip()).strip()
                vessel_link = self.URL % a['href']
                vessel_broken = '(Broken' in a.findChild().text.strip()
                imo_number = vessel_link.split('.')
                imo_number = imo_number[2].split('_')[1]
                already_exist = Vessel.objects.filter(imo_number=imo_number).exists()
                if not already_exist:
                    self.get_save_single_vessel_detail(vessel_name, vessel_broken, vessel_link)
        return all_vessels

    def get_save_single_vessel_detail(self, vessel_name, is_boken, vessel_url):
        self.VESSEL_COUNT = self.VESSEL_COUNT + 1
        vessel = Vessel()
        r = requests.get(vessel_url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find('table', style="width: 100%; text-align: left;")
            information = table.find_all('td')
            vessel.created_by = User.objects.get(username='immadimtiaz')
            vessel.imo_number = information[0].text.strip().split(':')[1].strip()
            vessel.broken = is_boken
            vessel.first_name = information[1].text.strip().split(':')[1]
            vessel.nationality = information[2].text.strip().split(':')[1]
            vessel.owner = information[3].text.strip().split(':')[1]
            operator = information[4].text.strip().split(':')[1]
            operator = operator.strip()

            vessel.operator = operator
            vessel.completion_year = information[5].text.strip().split(':')[1]
            vessel.shipyard = information[6].text.strip().split(':')[1]
            vessel.hull_number = information[7].text.strip().split(':')[1]
            vessel.engine_design = information[8].text.strip().split(':')[1]
            vessel.engine_type = information[9].text.strip().split(':')[1]
            vessel.engine_power_output = information[10].text.strip().split(':')[1]
            vessel.max_speed = information[11].text.strip().split(':')[1]
            vessel.over_all_length_m = information[12].text.strip().split(':')[1]
            vessel.over_all_beam_m = information[13].text.strip().split(':')[1]
            vessel.max_draught_m = information[14].text.strip().split(':')[1]
            vessel.max_TEU_capacity = information[15].text.strip().split(':')[1]
            vessel.container_capacity_at_14t_teu = information[16].text.strip().split(':')[1]
            vessel.reefer_containers_TEU = information[17].text.strip().split(':')[1]
            vessel.dead_weight_ton = information[18].text.strip().split(':')[1]
            vessel.gross_tonnage_ton = information[19].text.strip().split(':')[1]
            vessel.handling_gear = information[20].text.strip().split(':')[1]

            vessel.save()
        return
