#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Gönderilmedi listesinde gönderilenlerin hepsini otomatik olarak gönderildi
# işaretlemek için bir betik. CSV dosyasına ihtiyacımız var.
#
# Gökmen Görgen, <gkmngrgn_gmail.com>

import sys
import os

script_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.split(script_dir)[0]
sys.path.append(project_dir)
sys.path.append(os.path.split(project_dir)[0])
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import CITY_LIST
from shipit.models import CdClient

city_dict = {}
for i in CITY_LIST:
    city_dict[i[-1]] = i[0]


def main(csv_file_path):
    """Main function"""

    sent_list = get_sent_list(csv_file_path)

    if sent_list:
        mark_as_sent(sent_list)


def get_sent_list(csv_file_path):
    """Checking and opening for check_csv_file"""
    if os.path.splitext(csv_file_path)[-1] != '.csv':
        print("It's not a .csv file.")

        return False

    try:
        csv_file = file(csv_file_path, 'r')

        return csv_file.readlines()

    except IOError:
        print("Invalid file path. It doesn't exist file or \
it's not a file.")

        return False


def mark_as_sent(sent_list):
    """Mark as sent"""
    users = CdClient.objects.all()
    multiple_errors_file = open('multiple_errors.csv', 'w')
    m_error = 0
    not_exist_errors_file = open('not_exist_errors.csv', 'w')
    n_error = 0

    for sent in sent_list:
        phone_area, phone_number = get_phone(sent)
        first_name, last_name = get_name(sent)
        args = {
            'phone_area': phone_area,
            'phone_number': phone_number,
            'first_name': first_name,
            'last_name': last_name,
        }

        city = get_location(sent)
        if city != None:
            args['city'] = city

        try:
            user = users.get(**args)
            print("User: %s %s") % (user.first_name, user.last_name),
            if not user.sent:
                user.sent = 1 # True
                user.save()

                print("is marked as sent!")
            else:
                print("is already marked as send.")
        except CdClient.MultipleObjectsReturned:
            multiple_errors_file.write(sent)
            m_error += 1

        except CdClient.DoesNotExist:
            not_exist_errors_file.write(sent)
            n_error += 1

    multiple_errors_file.close()
    not_exist_errors_file.close()

    print("\nNumber of multiple user error: %s") % m_error
    print("Number of not exist error: %s") % n_error


def get_phone(csv_line):
    area, phone = csv_line.split(',')[-1].split(' ')
    area = area.replace('"(', '').replace(')', '')
    phone = phone.replace('"\n', '')

    return area, phone


def get_name(csv_line):
    name = csv_line.split(',')[0].split(' ')
    if len(name[:-1]) == 1:
        first_name = name[0]
    else:
        first_name = ' '.join(name[:-1])
    last_name = name[-1]

    return first_name.replace('"', ''), last_name.replace('"', '')


def get_location(csv_line):
    city = csv_line.split(',')[-2]

    try:
        return city_dict[city.replace('"', '')]
    except KeyError:
        return None


if __name__ == '__main__':
    args = sys.argv

    if len(args) != 2:
        print("""Invalid usage. Example:
$ python notsent2sent.py gonderilenler.csv""")
        sys.exit()

    csv_file = args[1]
    main(csv_file)
