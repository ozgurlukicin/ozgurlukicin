#!/usr/bin/python
# -*- coding: utf-8 -*-

import locale
from oi.shipit.models import CdClient
from xml.etree import ElementTree as ET


def add_column(limit):
    locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")
    cdclient = CdClient.objects.filter(confirmed=1, sent=0, taken=0).order_by('date')[:limit]
    root = ET.Element('document')

    for field in cdclient:
        cargo = ET.SubElement(root, 'cargo')

        receiver_name = ET.SubElement(cargo, 'receiver_name')
        receiver_name.text = '%s %s' % (field.first_name, field.last_name)

        receiver_address = ET.SubElement(cargo, 'receiver_address')
        receiver_address.text = field.address

        city = ET.SubElement(cargo, 'city')
        city.text = field.city

        town = ET.SubElement(cargo, 'town')
        town.text = field.town

        phone_work = ET.SubElement(cargo, 'phone_work')
        phone_gsm = ET.SubElement(cargo, 'phone_gsm')

        if field.phone_area.startswith('5'):
            phone_work.text = '0'
            phone_gsm.text = '%s%s' % (field.phone_area, field.phone_number)
        else:
            phone_work.text = '%s%s' % (field.phone_area, field.phone_number)
            phone_gsm.text = '0'

        email_address = ET.SubElement(cargo, 'email_address')
        email_address.text = field.email

        tax_number = ET.SubElement(cargo, 'tax_number')
        tax_number.text = field.tcidentity

        cargo_count = ET.SubElement(cargo, 'cargo_count')
        cargo_count.text = "1"

        cargo_type = ET.SubElement(cargo, 'cargo_type')
        cargo_type.text = "0"

        payment_type = ET.SubElement(cargo, 'payment_type')
        payment_type.text = "0"

        dispatch_number = ET.SubElement(cargo, 'dispatch_number')
        dispatch_number.text = "12343"

        referans_number = ET.SubElement(cargo, 'referans_number')
        referans_number.text = "1234"

        cargo_content = ET.SubElement(cargo, 'cargo_content')
        cargo_content.text = "Pardus Kurulum CD'si"

        collection_type = ET.SubElement(cargo, 'collection_type')
        collection_type.text = '0'

        invoice_number = ET.SubElement(cargo, 'invoice_number')
        invoice_number.text = '0000'

        invoice_amount = ET.SubElement(cargo, 'invoice_amount')
        invoice_amount.text = '2,36'

    tree = ET.ElementTree(root)
    tree.write('kargo.xml', encoding='utf-8')
