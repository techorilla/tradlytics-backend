import textract
from django.conf import settings
from doniServer.models import ShippingPort
import pycountry
from django.contrib.auth.models import User


created_by = User.objects.get(username='immadimtiaz')

SEA_PORT_PDF = '/dataSheets/seaports.pdf'

def save_all_ports():


    text = textract.process(settings.PROJECT_ROOT+SEA_PORT_PDF, method='pdftotext' )
    text_start = text[458:]
    port_details = text_start.split('\n')
    port_details = [detail for detail in port_details if detail != '']
    port_details_length = port_details.__len__()

    counter = 0

    while counter < port_details_length:
        is_country = False
        while not is_country:
            try:
                if counter == port_details_length:
                    break
                pycountry.countries.get(name=port_details[counter])
                is_country = True
            except KeyError:
                counter = counter + 1

        item = port_details[counter:counter+6]
        if item.__len__() == 6:
            new_port = ShippingPort()
            new_port.country = item[0]
            new_port.name = item[1]
            new_port.lo_code = item[2]
            new_port.location = item[3]
            new_port.contact_no = item[4]
            new_port.website = item[5]
            new_port.created_by = created_by
            new_port.save()
        counter = counter + 6













