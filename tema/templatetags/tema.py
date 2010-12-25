#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import template
from django.template import Context, loader
from oi.tema.models import ThemeAbuseReport
import datetime

register = template.Library()

@register.simple_tag
def number_of_theme_abuse():
    return ThemeAbuseReport.objects.count()

@register.simple_tag
def fresh_or_updated(item):
    delta = datetime.datetime.now() - item.update
    if delta.days < 11:
        if item.submit == item.update:
            result = "fresh"
        else:
            result = "updated"

        return "<img src=\"/media/img/tema/new/%s.png\" />" % result
    return ""
