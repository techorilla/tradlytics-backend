from string import ascii_lowercase
from doniScrapper.proxy_manager import ProxyManager
from bs4 import BeautifulSoup
from doniServer.models import BpBasic, Transaction, BusinessAppProfile, TrShipment
from doniServer.models.shipment import Vessel, ShippingPort
from django.contrib.auth.models import User
import requests
import re
import dateutil.parser

VESSEL_FINDER_URL = 'https://www.vesselfinder.com/vessels/%s-IMO-%s-MMSI-%s'

def get_port_by_containing_city_country(city, country):
    all_string = ' '.split(city.strip())
    for query in all_string:
        try:
            port = ShippingPort.objects.get(country__contains=country.strip, name__contains=query)
            return {
                u'id': port.id,
                u'lo_code': port.lo_code,
                u'name': port.name,
                u'country': port.country
            }
        except ShippingPort.DoesNotExist:
            pass
    return None



def get_vessel_position_for_all_business_app_profile():
    all_business_profiles = BusinessAppProfile.objects.all()
    for profile in all_business_profiles:
        business_not_shipped_info =  get_vessel_position_for_all_non_shipped(profile.business)
    return business_not_shipped_info


def get_vessel_position_for_all_non_shipped(business):
    return get_vessel_position_transactions(Transaction.get_expected_arrival(business))

def get_vessel_position_transactions(transactions=[]):
    return map(get_vessel_position_for_transaction, transactions)

def get_vessel_position_for_transaction(transaction):
    if transaction.shipment.vessel:
        return transaction.file_id, get_vessel_position(transaction.shipment.vessel)
    else:
        return transaction.file_id, None

def get_vessel_position(vessel):
    name = vessel.first_name if vessel.first_name else vessel.name
    name = name.upper().strip().replace(' ', '-')
    url = VESSEL_FINDER_URL%(name, vessel.imo_number, vessel.mmsi_number)
    response = requests.get(url, headers={'User-Agent': 'Google Chrome'})
    soup = BeautifulSoup(response.text, 'html.parser')
    longitude_element = soup.find("span", {'itemprop':'latitude'})
    latitude_element = soup.find("span", {'itemprop': 'longitude'})
    last_five_ports_elements = soup.find_all("div", {'itemtype':'http://schema.org/Event'})
    last_five_ports = []
    for port in last_five_ports_elements:
        arrival_date = port.find('span', {'class': 'small-5 medium-6 columns'}).text
        city_country = port.find('a').text.split(',')
        city_country.append(dateutil.parser.parse(arrival_date))
        last_five_ports.append(city_country)
    return longitude_element.text, latitude_element.text, last_five_ports




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
