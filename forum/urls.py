#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

from models import Forum, Category

main_dict = {
             'queryset': Forum.objects.filter(hidden=0).order_by('name'),
             'template_name': 'forum/main.html',
             'template_object_name': 'forum',
             'extra_context': {'categories': Category.objects.filter(hidden=0).order_by('name')}
            }

urlpatterns = patterns('',
    #(r'^feed/rss/$', 'rssfeed'),
    #(r'^feed/atom/$', 'atomfeed'),
    #(r'^feed/$', 'rssfeed'),

    #(r'^feed/atom/user/(?P<user>\d+)/$', 'atomfeed'),
    #(r'^feed/rss/user/(?P<user>\d+)/$', 'rssfeed'),

    (r'^$', 'django.views.generic.list_detail.object_list', dict(main_dict)),
)
