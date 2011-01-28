#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from oi.tema.models import ThemeItem, Wallpaper, DesktopScreenshot, Font, OpenOfficeTheme, IconSet, PackageScreenshot
from oi.settings import SITE_NAME, WEB_URL, SITE_DESC

category_dict = {"duvar-kagitlari": (Wallpaper, "Duvar Kağıtları", "duvar-kagitlari"),
                 "masaustu-goruntuleri": (DesktopScreenshot, "Ekran Görüntüleri", "masaustu-goruntuleri"),
                 "yazitipleri": (Font, "Yazıtipleri", "yazitipleri"),
                 "open-office": (OpenOfficeTheme, "Openoffice.org Öğeleri", "open-office"),
                 "simge-seti": (IconSet, "Simge Setleri", "simge-seti"),
                 "paket-goruntuleri": (PackageScreenshot, "Uygulama Görüntüleri", "paket-goruntuleri"),
        }

class RSS(Feed):
    title = "%s Temalar" % SITE_NAME
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

class User_RSS(Feed):
    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def title(self, obj):
        return "%s Tema Kullanıcı: %s" % (SITE_NAME, obj.username)

    def description(self, obj):
        return SITE_DESC

    def link(self, obj):
        return "%s/tema/kullanici/%s/" % (WEB_URL, obj.username)

    def items(self, obj):
        return ThemeItem.objects.filter(author=obj, status=True).order_by("-update")[:20]

    def item_link(self, item):
        return "%s%s" % (WEB_URL, item.get_absolute_url())

class User_Atom(User_RSS):
    feed_type = Atom1Feed
    subtitle = User_RSS.description

class Category_RSS(Feed):
    def get_object(self, request, category):
        try:
            return category_dict[category]
        except KeyError:
            raise FeedDoesNotExist

    def title(self, obj):
        return "%s %s" % (SITE_NAME, obj[1])

    def description(self, obj):
        return SITE_DESC

    def link(self, obj):
        return "%s/tema/%s/" % (WEB_URL, obj[2])

    def items(self, obj):
        return obj[0].objects.filter(status=True).order_by("-update")[:20]

    def item_link(self, item):
        return "%s%s" % (WEB_URL, item.get_absolute_url())

class Category_Atom(Category_RSS):
    feed_type = Atom1Feed
    subtitle = Category_RSS.description
