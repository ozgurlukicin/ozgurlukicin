#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

urlpatterns = patterns("",
    (r"^$", "oi.editor.views.list_articles"),
    (r"^haber/ekle/$", "oi.editor.views.create_contributednews"),
    (r"^haber/duzenle/(?P<news_id>\d+)/$", "oi.editor.views.change_contributednews"),
)
