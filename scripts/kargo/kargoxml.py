#!/usr/bin/python
# -*- coding: utf-8 -*-

import locale
import sys
import os

script_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
project_dir = os.path.split(script_dir)[0]
sys.path.append(project_dir)
sys.path.append(os.path.split(project_dir)[0])
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from oi.shipit.models import CdClient
from xml.etree import ElementTree as ET


def add_column(limit, timestamp):
    locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")
    cdclient = CdClient.objects.filter(confirmed=1,
        sent=0, taken=0).order_by('date')[:limit]
    root = ET.Element('document')

    for field in cdclient:
        cargo = ET.SubElement(root, 'cargo')
        sub_elements = {
            'receiver_name': '%s %s' % (field.first_name, field.last_name),
            'receiver_address': field.address,
            'city': field.city,
            'town': field.town,
            'email_address': field.email,
            'tax_number': field.tcidentity,
            'cargo_count': "1",
            'cargo_type': "0",
            'payment_type': "0",
            'dispatch_number': " ",
            'referans_number': " ",
            'cargo_content': "Pardus Kurulum CD'si",
            'collection_type': "0",
            'invoice_number': " ",
            'invoice_amount': "2,36"}

        for element in sub_elements:
            ET.SubElement(cargo, element).text = sub_elements[element]

        phone_work = ET.SubElement(cargo, 'phone_work')
        phone_gsm = ET.SubElement(cargo, 'phone_gsm')

        if field.phone_area.startswith('5'):
            phone_work.text = ' '
            phone_gsm.text = '%s%s' % (field.phone_area, field.phone_number)
        else:
            phone_work.text = '%s%s' % (field.phone_area, field.phone_number)
            phone_gsm.text = ' '

    tree = ET.ElementTree(root)
    tree.write('kargo_%s.xml' % timestamp, encoding='utf-8')
