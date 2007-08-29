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

def reply(request, forum_slug, topic_id):
    if not request.user.is_authenticated:
        raise HttpResponseServerError #FIXME: Give an error message

    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if forum.locked or topic.locked:
        raise HttpResponseServerError #FIXME: Give an error message

    if request.user.is_authenticated and request.method == 'POST':
        form = PostForm(request.POST.copy())
        if form.is_valid():
            post = Post(topic=topic,
                        author=request.user,
                        text=form.clean_data['text']
                       )
            post.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostForm(auto_id=True).as_p()

    return render_response(request, 'forum/new_topic.html', {'form': form})

def quote(request, forum_slug, topic_id, post_id):
    if not request.user.is_authenticated:
        raise HttpResponseServerError #FIXME: Give an error message

    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if forum.locked or topic.locked:
        raise HttpResponseServerError #FIXME: Give an error message

    if request.user.is_authenticated and request.method == 'POST':
        form = PostForm(request.POST.copy())
        if form.is_valid():
            post = Post(topic=topic,
                        author=request.user,
                        text=form.clean_data['text']
                       )
            post.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        post = get_object_or_404(Post, pk=post_id)

        if post in topic.post_set.all():
            form = PostForm(auto_id=True, initial={'text': '[quote|'+post_id+']'+post.text+'[/quote]'}).as_p()
        else:
            pass #Give an exception

    return render_response(request, 'forum/new_topic.html', {'form': form})

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