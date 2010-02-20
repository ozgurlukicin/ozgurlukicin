#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.views.generic.list_detail import object_list
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.views.generic.list_detail import object_list

from oi.st.wrappers import render_response
from oi.forum.forms import PostForm
from oi.podcast.models import *
from oi.podcast.settings import EPISODES_PER_PAGE
import oi.settings

def main(request):
    last_episode = Episode.objects.filter(status=True).order_by("-update")[0]
    episode_list = Episode.objects.filter(status=True).exclude(id=last_episode.id).order_by("-update")
    return object_list(request, episode_list,
            template_name="podcast/main.html",
            template_object_name="episode",
            extra_context={"last_episode":last_episode},
            paginate_by=EPISODES_PER_PAGE,
    )

def detail(request, slug):
    episode = get_object_or_404(Episode, slug=slug)
    form = PostForm()
    return render_response(request, 'podcast/detail.html', locals())

def feed(request):
    WEB_URL = oi.settings.WEB_URL
    episode_list = Episode.objects.filter(status=True).order_by("-update")
    xml = loader.get_template("podcast/feed.html").render(Context(locals()))
    return HttpResponse(xml, mimetype="application/xml")

def feed_ogg(request):
    WEB_URL = oi.settings.WEB_URL
    episode_list = Episode.objects.filter(status=True).order_by("-update")
    xml = loader.get_template("podcast/feed_ogg.html").render(Context(locals()))
    return HttpResponse(xml, mimetype="application/xml")
