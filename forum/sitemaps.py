#!/usr/bin/python
# -*- coding: utf-8 -*-#
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.


from django.contrib.sitemaps import Sitemap

from oi.forum.models import Topic

class TopicSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Topic.objects.filter(hidden=False)

    def lastmod(self, obj):
        return obj.topic_latest_post.edited
