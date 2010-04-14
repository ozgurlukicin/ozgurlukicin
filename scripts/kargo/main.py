#!/usr/bin/python
# -*- coding: utf-8 -*-

import locale
import os
import sys
from datetime import date

from kargoxml import add_column

script_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
project_dir = os.path.split(script_dir)[0]
sys.path.append(project_dir)
sys.path.append(os.path.split(project_dir)[0])
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from oi.shipit.models import CdClient


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print("Usage: python %s [limit]") % __file__
        sys.exit()

    try:
        limit = int(args[-1])
    except ValueError:
        print("Invalid limit: %s") % args[-1]
        sys.exit()

    locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")
    cdclient = CdClient.objects.filter(confirmed=1,
        sent=0, taken=0).order_by('date')[:limit]

    add_column(cdclient, date.today().isoformat())
