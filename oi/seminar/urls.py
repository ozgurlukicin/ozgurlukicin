#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

from oi.settings import SEMINAR_PER_PAGE

from oi.seminar.models import Seminar
from oi.profile.settings import googleMapsApiKey

seminar_list = {
                'queryset': Seminar.objects.filter(status=True),
                'template_name': 'seminar/seminar.html',
                'paginate_by': SEMINAR_PER_PAGE,
                'template_object_name': 'seminar'
               }

seminar = {
        "queryset": Seminar.objects.filter(status=True),
        "extra_context": {"apikey": googleMapsApiKey},
        }

urlpatterns = patterns('',
    (r'^liste/$', 'django.views.generic.list_detail.object_list', dict(seminar_list, page=1)),
    (r'^sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(seminar_list)),
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', dict(seminar)),
    (r'^konusmaci/(?P<attender>\d+)/$', 'oi.seminar.views.attender'),
    (r'^yer/(?P<place>\d+)/$', 'oi.seminar.views.place'),
)
