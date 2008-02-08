#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime
from django.template import Library
from django.utils.timesince import timesince

register = Library()

@register.filter
def timedelta(value, arg=None):
    if not value:
        return ''
    if arg:
        cmp = arg
    else:
        cmp = datetime.now()
    if value > cmp:
        return "%s sonra" % timesince(cmp,value)
    else:
        return "%s önce" % timesince(value,cmp)
