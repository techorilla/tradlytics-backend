from string import ascii_lowercase
from doniScrapper.proxy_manager import ProxyManager
from bs4 import BeautifulSoup
from doniServer.models import BpBasic
from doniServer.models.shipment import Vessel
from django.contrib.auth.models import User
import requests
import re

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
            vessel.imo_number = information[0].text.strip().split(':')[1]
            vessel.broken = is_boken
            vessel.first_name = information[1].text.strip().split(':')[1]
            vessel.nationality = information[2].text.strip().split(':')[1]
            vessel.owner = information[3].text.strip().split(':')[1]
            operator = information[4].text.strip().split(':')[1]
            operator = operator.strip()
            try:
                operator = BpBasic.objects.get(bp_name=operator)
            except BpBasic.DoesNotExist:
                self.SHIPPING_COMPANY_NOT_FOUND.append(operator)
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
        return
