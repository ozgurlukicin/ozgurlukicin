#!/usr/bin/python
# -*- coding: utf-8 -*-#
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.


from django.contrib.sitemaps import Sitemap

from oi.st.models import News, HowTo, Game, Package, FS, Workshop

class NewsSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0

    def items(self):
        return News.objects.filter(status=True).order_by('-update')

    def lastmod(self, obj):
        return obj.update

class HowToSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return HowTo.objects.filter(status=True).order_by('-update')

    def lastmod(self, obj):
        return obj.update

class GameSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Game.objects.filter(status=True).order_by('-update')

    def lastmod(self, obj):
        return obj.update

class PackageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Package.objects.filter(status=True).order_by('-update')

    def lastmod(self, obj):
        return obj.update

class FSSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return FS.objects.filter(status=True).order_by('-update')

    def lastmod(self, obj):
        return obj.update

class WorkshopSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Workshop.objects.filter(status=True).order_by('-update')

    def lastmod(self, obj):
        return obj.update
