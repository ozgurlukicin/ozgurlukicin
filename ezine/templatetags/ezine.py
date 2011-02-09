#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.template import Library
from oi.settings import MEDIA_URL
from oi.ezine.models import Ezine

register = Library()

@register.simple_tag
def current_ezine_image():
    current_ezine = Ezine.objects.filter(is_active=True).order_by("-issue")[0]
    return "%s%s" % (MEDIA_URL, current_ezine.image.file.name)
