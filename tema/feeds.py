#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import FeedDoesNotExist

from oi.tema.models import ThemeItem
from oi.settings import SITE_NAME, WEB_URL, SITE_DESC

class RSS(Feed):
    title = "%s - Temalar" % SITE_NAME
    link = WEB_URL
    description = SITE_DESC

    def items(self):
        return ThemeItem.objects.filter(status=True).order_by("-update")[:40]

    def item_author_name(self, item):
        return item.author

    def item_pubdate(self, item):
        return item.update

    def item_categories(self, item):
        return [tag.name for tag in item.tags.all()]

class Atom(RSS):
    feed_type = Atom1Feed
    subtitle = RSS.description
