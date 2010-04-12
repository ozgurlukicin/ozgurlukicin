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

from shipit.models import CdClient


def main(csv_file_path):
    """Main function"""

    sent_list = get_sent_list(csv_file_path)

    if not sent_list:
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

if __name__ == '__main__':
    args = sys.argv

    if len(args) != 2:
        print("""Invalid usage. Example:
$ python notsent2sent.py gonderilenler.csv""")
        sys.exit()

    csv_file = args[1]
    main(csv_file)
