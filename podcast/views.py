#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.views.generic.list_detail import object_list
from django.http import HttpResponse
from django.template import Context, loader

from oi.st.wrappers import render_response
from oi.podcast.models import *
import oi.settings

def main(request):
    episode_list = Episode.objects.filter(status=True)
    return render_response(request, 'podcast/main.html', locals())

def feed(request):
    WEB_URL = oi.settings.WEB_URL
    episode_list = Episode.objects.filter(status=True)
    xml = loader.get_template("podcast/feed.html").render(Context(locals()))
    return HttpResponse(xml, mimetype="application/xml")
