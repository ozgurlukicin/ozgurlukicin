#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from oi.forum.models import *
from oi.settings import SITE_NAME, WEB_URL, SITE_DESC

class RSS(Feed):
    title = SITE_NAME + "Forum"
    link = WEB_URL
    description = SITE_DESC
    title_template = 'forum/feed_title.html'
    description_template = 'forum/feed_description.html'

    def items(self):
        return Post.objects.filter(hidden=0).order_by('-edited')[:10]

class Atom(RSS):
    feed_type = Atom1Feed
    subtitle = RSS.description