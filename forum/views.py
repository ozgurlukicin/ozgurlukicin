#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from oi.forum.settings import *
from oi.forum.forms import *

from oi.st.wrappers import render_response
from oi.forum.models import Category, Forum, Topic, Post, AbuseReport, WatchList

def main(request):
    forums = Forum.objects.order_by('name')

    return render_response(request, 'forum/forum_list.html', locals())

def forum(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topics = forum.topic_set.all().order_by('-sticky', '-topic_latest_post')

    return object_list(request, topics, template_name='forum/forum_detail.html', template_object_name='topic', extra_context={'forum': forum}, paginate_by=TOPICS_PER_PAGE, allow_empty=True)

def topic(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    posts = topic.post_set.all().order_by('created')

    session_key = 'visited_'+topic_id

    if request.user.is_authenticated() and not session_key in request.session:
        topic.views += 1
        request.session[session_key] = True
        topic.save()

    return render_response(request, 'forum/topic.html', locals())

@login_required
def reply(request, forum_slug, topic_id, post_id=False):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if forum.locked or topic.locked:
        raise HttpResponseServerError #FIXME: Give an error message

    if request.method == 'POST':
        form = PostForm(request.POST.copy())

        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            post = Post(topic=topic,
                        author=request.user,
                        text=form.cleaned_data['text']
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
def edit_post(request, forum_slug, topic_id, post_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    post = get_object_or_404(Post, pk=post_id)

    if forum.locked or topic.locked:
        raise HttpResponseServerError #FIXME: Give an error message

    if request.method == 'POST':
        form = PostForm(request.POST.copy())

        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            post.text = form.cleaned_data['text']
            post.edit_count += 1
            post.edited = datetime.now()
            post.last_edited_by = request.user
            post.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        if post in topic.post_set.all():
            form = PostForm(auto_id=True, initial={'text': post.text})

    return render_response(request, 'forum/reply.html', locals())

@login_required
def new_topic(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug)

    if forum.locked:
        raise HttpResponseServerError #FIXME: Give an error message

    if request.method == 'POST':
        form = TopicForm(request.POST.copy())
        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            topic = Topic(forum=forum,
                          title=form.cleaned_data['title']
                         )
            topic.save()

            post = Post(topic=topic,
                        author=request.user,
                        text=form.cleaned_data['text']
                       )
            post.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = TopicForm(auto_id=True)

    return render_response(request, 'forum/new_topic.html', locals())

@login_required
def edit_topic(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    first_post = topic.post_set.order_by('created')[0]

    if forum.locked or topic.locked:
        raise HttpResponseServerError #FIXME: Give an error message

    if request.method == 'POST':
        form = TopicForm(request.POST.copy())
        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            topic.title = form.cleaned_data['title']
            topic.topic_latest_post = first_post
            topic.save()

            first_post.edit_count += 1
            first_post.edited = datetime.now()
            first_post.last_edited_by = request.user
            first_post.save()

            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        form = TopicForm(auto_id=True, initial={'title': topic.title, 'text': first_post.text})

    return render_response(request, 'forum/new_topic.html', locals())

@login_required
def hide(request, forum_slug, topic_id, post_id=False):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.user.has_perm('post.can_hide') and post_id:
        post = get_object_or_404(Post, pk=post_id)

        if post.hidden:
            post.hidden = 0
        else:
            post.hidden = 1

        post.save()

        return HttpResponseRedirect(topic.get_absolute_url())

    if request.user.has_perm('topic.can_hide') and not post_id:
        if topic.hidden:
            topic.hidden = 0
        else:
            topic.hidden = 1

        topic.save()

        return HttpResponseRedirect(forum.get_absolute_url())

@login_required
def stick(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.user.has_perm('topic.can_stick') and not topic.sticky:
        topic.sticky = 1
        topic.save()

        return HttpResponseRedirect(forum.get_absolute_url())

    if request.user.has_perm('topic.can_stick') and topic.sticky:
        topic.sticky = 0
        topic.save()

        return HttpResponseRedirect(forum.get_absolute_url())

@login_required
def lock(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.user.has_perm('topic.can_lock') and not topic.locked:
        topic.locked = 1
        topic.save()

        return HttpResponseRedirect(forum.get_absolute_url())

    if request.user.has_perm('topic.can_lock') and topic.locked:
        topic.locked = 0
        topic.save()

        return HttpResponseRedirect(forum.get_absolute_url())

def flood_control(request):
    if 'flood_control' in request.session and ((datetime.now() - request.session['flood_control']).seconds < FLOOD_TIMEOUT):
        flood = True
        timeout = (FLOOD_TIMEOUT - (datetime.now() - request.session['flood_control']).seconds)
    if not 'flood_control' in request.session or ((datetime.now() - request.session['flood_control']).seconds > FLOOD_TIMEOUT):
        flood = False
        timeout = False
        request.session['flood_control'] = datetime.now()

    return flood,timeout
