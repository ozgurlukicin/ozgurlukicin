#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import template
from oi.tema.models import ThemeAbuseReport

register = template.Library()

@register.simple_tag
def number_of_theme_abuse():
    return ThemeAbuseReport.objects.count()

