#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAEpr
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from oi.tema.models import ThemeItem
from oi.settings import SITE_NAME, WEB_URL, SITE_DESC

from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from django.utils.translation import ugettext as _

class Tema_RSS(Feed):
    title = SITE_NAME + _("Themes")
    link = WEB_URL
    description = SITE_DESC + _("Wallpapers, fonts and more.")
    title_template = 'tema/feed_title.html'
    description_template = 'tema/feed_description.html'

    def items(self):
        return File.objects.filter(state=True).order_by("-update")[:10]


class Tema_Atom(Tema_RSS):
    feed_type = Atom1Feed
    subtitle = Tema_RSS.description


class Category_Tema_Rss(Feed):
    title_template = 'forum/feed_title.html'
    description_template = 'forum/feed_description.html'

    def get_object(self,bits):
        """ The forum object
        (r'^(?P<url>.*)/topic/(?P<topic_id>\d+)/$' for that kind of urls
        """
        if not len(bits)==1:
            raise ObjectDoesNotExist

        return ParentCategory.objects.get(id=bits[0])

    def title(self,obj):
        return SITE_NAME + " Tema Kategori : %s" % obj.category

    def link(self,obj):
        if not obj:
            raise FeedDoesNotExist
        return "%s%s" % (WEB_URL, obj.get_absolute_url())

    def description(self,obj):
        return SITE_DESC

    def items(self,obj):
        return ThemeItem.objects.filter(category=obj,approved=True).order_by('-edit_date')[:20]

    def item_link(self, item):
        if not item:
            raise FeedDoesNotExist
        return "%s%s" % (WEB_URL, item.get_absolute_url())

class Category_Tema_Atom(Category_Tema_Rss):
    """ Category Atom"""
    feed_type = Atom1Feed
    subtitle = Category_Tema_Rss.description

class User_Tema_Rss(Feed):
    title_template = 'forum/feed_title.html'
    description_template = 'forum/feed_description.html'

    def get_object(self,bits):
        if not len(bits)==1:
            raise ObjectDoesNotExist

        return User.objects.get(id=bits[0])

    def title(self,obj):
        return _("%(site_name)s Theme: %(username)s") % {"site_name":SITE_NAME, "username":obj.username}

    def description(self,obj):
        return SITE_DESC

    def link(self,obj):
        if not obj:
            raise FeedDoesNotExist
        return "%s/tema/kullanici/%s/" % (WEB_URL, obj.username)

    def items(self,obj):
        return ThemeItem.objects.filter(author=obj,approved=True).order_by('-edit_date')[:20]

    def item_link(self, item):
        if not item:
            raise FeedDoesNotExist
        return "%s%s" % (WEB_URL, item.get_absolute_url())

class User_Tema_Atom(User_Tema_Rss):
    feed_type = Atom1Feed
    subtitle = User_Tema_Rss.description
