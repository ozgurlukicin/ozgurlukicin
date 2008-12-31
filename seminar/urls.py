#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

from oi.seminar.models import Seminar
from oi.profile.settings import googleMapsApiKey

seminar = {
        "queryset": Seminar.objects.filter(status=True),
        "extra_context": {"apikey": googleMapsApiKey},
        }

urlpatterns = patterns('',
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', dict(seminar)),
)
