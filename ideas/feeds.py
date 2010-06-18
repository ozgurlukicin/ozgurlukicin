#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed

from oi.settings import SITE_NAME, WEB_URL, SITE_DESC
from oi.ideas.models import Idea
from django.utils.translation import ugettext as _

class RSS(Feed):
    title = SITE_NAME + _(" Brainstorm")
    link = WEB_URL
    description = SITE_DESC

    def items(self):
        objects = Idea.objects.filter(is_hidden=False).order_by('-submitted_date')[:40]
        return objects

    def item_author_name(self, item):
        return item.submitter

    def item_pubdate(self, item):
        return item.submitted_date

    def item_categories(self, item):
        return [tag.name for tag in item.tags.all()]

class Atom(RSS):
    feed_type = Atom1Feed
    subtitle = RSS.description
