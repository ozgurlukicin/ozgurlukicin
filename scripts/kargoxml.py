#!/usr/bin/python
# -*- coding: utf-8 -*-

import locale
from oi.shipit.models import CdClient
from xml.etree import ElementTree as ET


def add_column(cargo):
    locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")
    cdclient = CdClient.objects.filter(confirmed=1, sent=0, taken=0)[:300]
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
        phone_work.text = '%d%d' % (field.phone_area, field.phone_number)

        phone_gsm = ET.SubElement(cargo, 'phone_gsm')
        phone_gsm.text = '0'

        email_address = ET.SubElement(cargo, 'email_address')
        email_address.text = field.email

        tax_number = ET.SubElement(cargo, 'tax_number')
        tax_number.text = field.tcidentity

        cargo_count = ET.SubElement(cargo, 'cargo_count')
        cargo_count = "1"

        cargo_type = ET.SubElement(cargo, 'cargo_type')
        cargo_type.text = "1"

        payment_type = ET.SubElement(cargo, 'payment_type')
        payment_type = "0"

        dispatch_number = ET.SubElement(cargo, 'dispatch_number')
        dispatch_number = "12343"

        referans_number = ET.SubElement(cargo, 'referans_number')
        referans_number = "1234"

        cargo_content = ET.SubElement(cargo, 'cargo_content')
        cargo_content.text = "Pardus Kurulum CD'si"

        collection_type = ET.SubElement(cargo, 'collection_type')
        collection_type = '0'

        invoice_number = ET.SubElement(cargo, 'invoice_number')
        invoice_number.text = 'yk123'

        invoice_amount = ET.SubElement(cargo, 'invoice_amount')
        invoice_amount.text = '12'

    tree = ET.ElementTree(root)
    tree.write('kargo.xml')
