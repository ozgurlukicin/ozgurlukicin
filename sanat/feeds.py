#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbulpr
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from oi.sanat.models import Dosya 
from oi.settings import SITE_NAME, WEB_URL, SITE_DESC

class Tema_RSS(Feed):
    title = SITE_NAME + "Temalar"
    link = WEB_URL
    description = SITE_DESC + "Pencere dekorasyonları, duvar kağıtları ve daha fazlası."
    title_template = 'sanat/feed_title.html'
    description_template = 'sanat/feed_description.html'

    def items(self):
        return Dosya.objects.filter(state=True).order_by("-update")[:10]

class Tema_Atom(Tema_RSS):
    feed_type = Atom1Feed
    subtitle = Tema_RSS.description
