#!/usr/bin/python
# -*- coding: utf-8 -*-#
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.


from django.contrib.sitemaps import Sitemap

from oi.st.models import News

class NewsSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0

    def items(self):
        return News.objects.filter(status=True).order_by('-update')

    def lastmod(self, obj):
        return obj.update
