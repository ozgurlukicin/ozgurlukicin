#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.paginator import ObjectPaginator

from oi.forum.settings import *

from oi.forum.forms import TopicForm, PostForm

from oi.st.wrappers import render_response
from oi.forum.models import Category, Forum, Topic, Post, AbuseReport, WatchList

def main(request):
    forums = Forum.objects.order_by('name')

    return render_response(request, 'forum/forum_list.html', locals())

def forum(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topics = forum.topic_set.all()
    #paginator = ObjectPaginator(topics, TOPICS_PER_PAGE)

    return render_response(request, 'forum/forum_detail.html', locals())

def topic(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    posts = topic.post_set.all().order_by('update')

    session_key = 'visited_'+topic_id

    if request.user.is_authenticated() and not session_key in request.session:
        topic.views += 1
        request.session[session_key] = True
        topic.save()

    return render_response(request, 'forum/topic.html', locals())

@login_required
def reply(request, forum_slug, topic_id, post_id=False):
    if not request.user.is_authenticated:
        raise HttpResponseServerError #FIXME: Give an error message

    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if forum.locked or topic.locked:
        raise HttpResponseServerError #FIXME: Give an error message

    if request.user.is_authenticated and request.method == 'POST':
        form = PostForm(request.POST.copy())

        if 'flood_control' in request.session and ((datetime.now() - request.session['flood_control']).seconds < FLOOD_TIMEOUT):
            flood = True
            timeout = (FLOOD_TIMEOUT - (datetime.now() - request.session['flood_control']).seconds)
        if not 'flood_control' in request.session or ((datetime.now() - request.session['flood_control']).seconds > FLOOD_TIMEOUT):
            flood = False
            request.session['flood_control'] = datetime.now()

        if form.is_valid() and not flood:
            post = Post(topic=topic,
                        author=request.user,
                        text=form.clean_data['text']
                       )
            post.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        if post_id:
            post = get_object_or_404(Post, pk=post_id)

            if post in topic.post_set.all():
                form = PostForm(auto_id=True, initial={'text': '[quote|'+post_id+']'+post.text+'[/quote]'})
        else:
            form = PostForm(auto_id=True)

    return render_response(request, 'forum/reply.html', locals())

@login_required
def new_topic(request, forum_slug):
    if not request.user.is_authenticated:
        raise HttpResponseServerError #FIXME: Give an error message

    if request.user.is_authenticated and request.method == 'POST':
        forum = get_object_or_404(Forum, slug=forum_slug)

        if forum.locked:
            raise HttpResponseServerError #FIXME: Give an error message

        form = TopicForm(request.POST.copy())
        if form.is_valid():
            topic = Topic(forum=forum,
                          title=form.clean_data['title']
                         )
            topic.save()

            post = Post(topic=topic,
                        author=request.user,
                        text=form.clean_data['text']
                       )
            post.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = TopicForm(auto_id=True).as_p()

    return render_response(request, 'forum/new_topic.html', {'form': form})