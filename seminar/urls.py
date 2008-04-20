#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

from oi.settings import SEMINAR_PER_PAGE

from oi.seminar.models import Seminar

seminar_dict = {
                'queryset': Seminar.objects.all(),
                'template_name': 'seminar/seminar.html',
                'paginate_by': SEMINAR_PER_PAGE,
                'template_object_name': 'seminar'
               }

urlpatterns = patterns('',
    (r'^liste/$', 'django.views.generic.list_detail.object_list', dict(seminar_dict, page=1)),
    (r'^sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(seminar_dict)),
    (r'^konusmaci/(?P<attender>\d+)/$', 'oi.seminar.views.attender'),
    (r'^yer/(?P<place>\d+)/$', 'oi.seminar.views.place'),

    (r'^feed/rss/$', 'oi.seminar.views.rss'),
    (r'^feed/atom/$', 'oi.seminar.views.atom'),
    (r'^feed/$', 'oi.seminar.views.rss'),

    (r'^feed/city/(?P<city>\d+)/atom/$', 'oi.seminar.views.atom'),
    (r'^feed/city/(?P<city>\d+)/rss/$', 'oi.seminar.views.rss'),
    (r'^feed/city/(?P<city>\d+)/$', 'oi.seminar.views.rss'),
)
