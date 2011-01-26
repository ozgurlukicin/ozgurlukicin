#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import FeedDoesNotExist

from oi.beyin2.models import Idea
from oi.settings import SITE_NAME, WEB_URL, SITE_DESC

class RSS(Feed):
    title = "%s - Beyin Fırtınası" % SITE_NAME
    link = WEB_URL
    description = SITE_DESC

    def items(self):
        return Idea.objects.filter(is_hidden=False).order_by("-dateSubmitted")[:40]

    def item_author_name(self, item):
        return item.submitter

    def item_pubdate(self, item):
        return item.dateSubmitted

    def item_categories(self, item):
        return [tag.name for tag in item.tags.all()]

class Atom(RSS):
    feed_type = Atom1Feed
    subtitle = RSS.description
