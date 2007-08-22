#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

from models import Topic, Forum, Category

main_dict = {
             'queryset': Forum.objects.filter(hidden=0).order_by('name'),
             'template_name': 'forum/forum_list.html',
             'template_object_name': 'forum',
             'extra_context': {'categories': Category.objects.filter(hidden=0).order_by('name')}
            }

forum_dict = {
              'queryset': Forum.objects.all(),
              'template_name': 'forum/topic_list.html',
              'template_object_name': 'forum',
              'slug_field': 'slug',
              'extra_context': {'topics': Topic.objects.filter(hidden=0).order_by('-sticky', '-topic_latest_post')}
             }

urlpatterns = patterns('',
    #(r'^feed/rss/$', 'rssfeed'),
    #(r'^feed/atom/$', 'atomfeed'),
    #(r'^feed/$', 'rssfeed'),

    #(r'^feed/atom/user/(?P<user>\d+)/$', 'atomfeed'),
    #(r'^feed/rss/user/(?P<user>\d+)/$', 'rssfeed'),

    (r'^$', 'django.views.generic.list_detail.object_list', dict(main_dict)),
    (r'^(?P<slug>.*)/$', 'django.views.generic.list_detail.object_detail', dict(forum_dict)),
)
