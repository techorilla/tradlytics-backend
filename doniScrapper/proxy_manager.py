import requests
from requests.exceptions import ConnectionError, ChunkedEncodingError
import random
# from core import log
import os
import time
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout

from TorCtl import TorCtl

class ProxyManager(object):

    def __init__(self):
        self.ipCheck = 'http://icanhazip.com/'
        self.proxy_list = []
        self.torhashedPassword = 'mypassword'
        self.useragents = self.load_user_agents('./doniScrapper/user_agents.txt')
        self.proxy_list += self.proxyforEU_url_parser('http://proxyfor.eu/geo.php', 100.0)
        self.proxy_list += self.freeProxy_url_parser('http://free-proxy-list.net')

    def change_my_ip_connection(self):
        conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase=self.hashed)
        conn.send_signal("NEWNYM")
        conn.close()

    def load_user_agents(self, useragentsfile):
        useragents = []
        with open(useragentsfile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    useragents.append(ua.strip()[1:-1 - 1])
        return useragents

    def get_random_user_agent(self):
        user_agent = random.choice(self.useragents)
        return user_agent

    def proxyforEU_url_parser(self, web_url, speed_in_KBs = 100.0):
        content = requests.get(web_url).content
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", attrs={"class": "proxy_list"})
        curl_proxy_list = []
        headings = [th.get_text() for th in table.find("tr").find_all("th")]
        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)
        for dataset in datasets:
            proxy = "http://"
            proxy_straggler = False
            for field in dataset:
                if field[0] == 'Speed':
                    if float(field[1]) < speed_in_KBs:
                        proxy_straggler = True
                if field[0] == 'IP':
                    proxy = proxy + field[1] + ':'
                elif field[0] == 'Port':
                    proxy = proxy + field[1]
            if not proxy_straggler:
                curl_proxy_list.append(proxy.__str__())
        return curl_proxy_list

    def freeProxy_url_parser(self, web_url):
        curl_proxy_list = []
        content = requests.get(web_url).content
        soup = BeautifulSoup(content, "html.parser")

        table = soup.find("table", attrs={"class": "display fpltable"})
        headings = [th.get_text() for th in table.find("tr").find_all("th")]
        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        for dataset in datasets:
            proxy = "http://"
            for field in dataset:
                if field[0] == 'IP Address':
                    proxy = proxy + field[1] + ':'
                elif field[0] == 'Port':
                    proxy = proxy + field[1]
            if proxy != 'http://':
                curl_proxy_list.append(proxy.__str__())
        return curl_proxy_list

    def generate_random_request_headers(self):
        headers = {
            "Connection": "close",  # another way to cover tracks
            "User-Agent": self.get_random_user_agent()
        }
        return headers



    def generate_proxied_request(self, url, params={}, req_timeout=30):
        if len(self.proxy_list) < 2:
            self.proxy_list += self.proxyForEU_url_parser('http://proxyfor.eu/geo.php')
        random.shuffle(self.proxy_list)
        req_headers = dict(params.items() + self.generate_random_request_headers().items())
        request = None
        try:
            rand_proxy = random.choice(self.proxy_list)
            request = requests.get(url, proxies={"http": rand_proxy},headers = req_headers, timeout = req_timeout)
            ip = rand_proxy

        except ConnectionError:
            self.proxy_list.remove(rand_proxy)
            # log.exception("Proxy unreachable - Removed Straggling proxy :", rand_proxy, " PL Size = ", len(self.proxy_list))
            return None,None, None
        except ReadTimeout:
            self.proxy_list.remove(rand_proxy)
            # log.exception("Read timed out - Removed Straggling proxy :", rand_proxy, " PL Size = ", len(self.proxy_list))
            return None,None, None
        return request.content, request.status_code, ip