#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET


def add_column(cdclient, timestamp, version):
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
            'invoice_amount': "2,36",
            'phone_work': '%s%s' % (field.phone_area, field.phone_number),
            'phone_gsm': '%s%s' % (field.gsm_area, field.gsm_number)}

        for element in sub_elements:
            ET.SubElement(cargo, element).text = sub_elements[element]

    tree = ET.ElementTree(root)
    tree.write('kargo_%s_%s.xml' % (timestamp, version), encoding='utf-8')
