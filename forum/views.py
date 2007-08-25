#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.paginator import ObjectPaginator

from oi.forum.settings import *

from oi.st.wrappers import render_response
from oi.forum.models import Category, Forum, Topic, Post, Moderator, AbuseReport, WatchList

def main(request):
    forums = Forum.objects.filter(hidden=0).order_by('name')

    return render_response(request, 'forum/forum_list.html', locals())

def forum(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topics = forum.topic_set.all()
    paginator = ObjectPaginator(topics, TOPICS_PER_PAGE)

    return render_response(request, 'forum/forum_detail.html', locals())

def topic(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    posts = topic.post_set.all().order_by('update')

    topic.views += 1
    topic.save()

    return render_response(request, 'forum/topic.html', locals())

def reply(request, forum, thread):
    """
    If a thread isn't closed, and the user is logged in, post a reply
    to a thread. Note we don't have "nested" replies at this stage.
    """
    if not request.user.is_authenticated:
        raise HttpResponseServerError

    f = get_object_or_404(Forum, slug=forum)
    t = get_object_or_404(Topic, pk=thread)

    if t.closed:
        raise HttpResponseServerError

    body = request.POST.get('body', False)
    p = Post(
        thread=t,
        author=request.user,
        body=body,
        time=datetime.now(),
        )
    p.save()
    return HttpResponseRedirect(p.get_absolute_url())

def newthread(request, forum):
    """
    Rudimentary post function - this should probably use 
    newforms, although not sure how that goes when we're updating 
    two models.

    Only allows a user to post if they're logged in.
    """
    if not request.user.is_authenticated:
        raise HttpResponseServerError
    f = get_object_or_404(Forum, slug=forum)
    t = Topic(
        forum=f,
        title=request.POST.get('title'),
    )
    t.save()
    p = Post(
        thread=t,
        author=request.user,
        body=request.POST.get('body'),
        time=datetime.now(),
    )
    p.save()
    return HttpResponseRedirect(t.get_absolute_url())
