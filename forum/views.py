#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from oi.forum.settings import *
from oi.forum.forms import *

from oi.st.wrappers import render_response
from oi.forum.models import Category, Forum, Topic, Post, AbuseReport, WatchList
from oi.forum import customgeneric

from django.core.urlresolvers import reverse
from oi.st.models import Tag, News

def main(request):
    lastvisit_control(request)

    categories = Category.objects.order_by('order')
    categories = [(category, category.forum_set.all()) for category in categories]
    forums = topics = posts = 0
    for category in categories:
        for forum in category[1]:
            forums += 1
            topics += forum.topics
            posts += forum.posts

            # read/unread stuff
            if forum.id in request.session["read_forum_dict"]:
                if forum.topics == request.session["read_forum_dict"][forum.id]:
                    forum.is_read = True
                else:
                    forum.is_read = False

    usercount = User.objects.count()
    currentdate = datetime.now()
    latest_posts = Post.objects.filter(hidden=False).order_by("-created")[:5]

    return render_response(request, 'forum/forum_list.html', locals())

def forum(request, forum_slug):
    lastvisit_control(request)

    forum = get_object_or_404(Forum, slug=forum_slug)
    topics = forum.topic_set.all().order_by('-sticky', '-topic_latest_post')

    if request.user.is_authenticated():
        for topic in topics:
            if topic.topic_latest_post.edited > request.session['last_visit'] or\
                    topic.id in request.session["read_topic_set"]:
                topic.is_read = True
            else:
                topic.is_read = False

    return customgeneric.object_list(request, topics,
                       template_name = 'forum/forum_detail.html',
                       template_object_name = 'topic',
                       extra_context = {'forum': forum},
                       paginate_by = TOPICS_PER_PAGE,
                       allow_empty = True)

def topic(request, forum_slug, topic_id):
    lastvisit_control(request)

    topic = get_object_or_404(Topic, pk=topic_id)
    forum = topic.forum
    if forum.slug != forum_slug:
        return HttpResponseRedirect(topic.get_absolute_url())
    posts = topic.post_set.all().order_by('created')
    news_list = News.objects.filter(status=1).order_by('-update')[:3]

    if request.user.is_authenticated() and not topic.id in request.session["read_topic_set"]:
        request.session["read_topic_set"].add(topic.id)
        if not forum.id in request.session["read_forum_dict"]:
            request.session["read_forum_dict"][forum.id] = 1
        else:
            request.session["read_forum_dict"][forum.id] += 1
        request.session.modified = True

    topic.views += 1
    topic.save()
    # we love Django, just 1 line and pagination is ready :)
    return object_list(request, posts,
                       template_name = 'forum/topic.html',
                       template_object_name = 'post',
                       extra_context = {'forum': forum, 'topic': topic, 'news_list':news_list, 'request': request},
                       paginate_by = POSTS_PER_PAGE,
                       allow_empty = True)

@login_required
def reply(request, forum_slug, topic_id, post_id=False):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    posts = topic.post_set.all().order_by('-created')[:POSTS_PER_PAGE]

    if forum.locked or topic.locked:
        return HttpResponse("Forum or topic is locked") #FIXME: Give an error message

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
    posts = topic.post_set.filter(created__lt = post.created).order_by('-created')[:POSTS_PER_PAGE]

    #the normal users dont have that permission actually
    if not request.user.has_perm('forum.change_post'):
        user=get_object_or_404(User, username=request.user.username)
        post_user=user.post_set.filter(id=post_id)

        if not post_user:
            return HttpResponse("That is a Wrong way my friend :) ")

    if forum.locked or topic.locked:
        # FIXME: Give an error message
        return HttpResponse("Forum or topic is locked")

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

    return render_response(request, 'forum/post_edit.html', locals())

@login_required
def new_topic(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug)

    if forum.locked:
        return HttpResponse('Forum is locked')

    if request.method == 'POST':
        form = TopicForm(request.POST.copy())
        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            topic = Topic(forum=forum,
                          title=form.cleaned_data['title'])
        #tags
            topic.save()

            for tag in form.cleaned_data['tags']:
                t=Tag.objects.get(name=tag)
                topic.tags.add(t)

            post = Post(topic=topic,
                        author=request.user,
                        text=form.cleaned_data['text'])

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

    if not request.user.has_perm('forum.change_topic'):
        return HttpResponse('Opps, wrong way :)')

    if forum.locked or topic.locked:
        return HttpResponse('Forum or topic is locked')

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
def merge(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if forum.locked or topic.locked:
        hata="Kilitli konularda bu tür işlemler yapılamaz!"
        return render_response(request, 'forum/merge.html', locals())

    if request.method == 'POST' and request.user.has_perm('forum.can_merge_topic'):
        form = MergeForm(request.POST.copy())
        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            topic2 = form.cleaned_data['topic2']

            if int(topic2)==topic.id:
                hata="Aynı konuyu mu merge edeceksiniz !"
                return render_response(request, 'forum/merge.html', locals())


            topic2_object=get_object_or_404(Topic, pk=int(topic2))

            posts_tomove=Post.objects.filter(topic=topic.id)
            for post in posts_tomove:
                post.topic = topic2_object
                post.save()

            #bir de simdi ileti sayisini arttirmak gerekir.
            topic2_object.posts += posts_tomove.count()
            topic2_object.save()

            topic.delete()

            return HttpResponseRedirect(forum.get_absolute_url())

        else:
            hata="Forum valid degil veya floood yapıyorsun!"
            return render_response(request, 'forum/merge.html', locals())

    else:
        form = MergeForm(auto_id=True)

    return render_response(request, 'forum/merge.html', locals())

@login_required
def hide(request, forum_slug, topic_id, post_id=False):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.user.has_perm('forum.can_hide_post') and post_id:
        post = get_object_or_404(Post, pk=post_id)

        if post.hidden:
            post.hidden = 0
        else:
            post.hidden = 1

        post.save()

        return HttpResponseRedirect(topic.get_absolute_url())
    elif request.user.has_perm('forum.can_hide_topic') and not post_id:
        if topic.hidden:
            topic.hidden = 0
        else:
            topic.hidden = 1

        topic.save()

        return HttpResponseRedirect(forum.get_absolute_url())
    else:
        return HttpResponseServerError # FIXME: Given an error message

@login_required
def stick(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.user.has_perm('forum.can_stick_stopic') and not topic.sticky:
        topic.sticky = 1
        topic.save()

        return HttpResponseRedirect(forum.get_absolute_url())
    elif request.user.has_perm('forum.can_stick_topic') and topic.sticky:
        topic.sticky = 0
        topic.save()

        return HttpResponseRedirect(forum.get_absolute_url())
    else:
        return HttpResponseServerError # FIXME: Give an error message

@login_required
def lock(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.user.has_perm('forum.can_lock_topic') and not topic.locked:
        topic.locked = 1
        topic.save()

        return HttpResponseRedirect(forum.get_absolute_url())
    elif request.user.has_perm('forum.can_lock_topic') and topic.locked:
        topic.locked = 0
        topic.save()

        return HttpResponseRedirect(forum.get_absolute_url())
    else:
        return HttpResponseServerError # FIXME: Give an error message

def flood_control(request):
    if 'flood_control' in request.session and ((datetime.now() - request.session['flood_control']).seconds < FLOOD_TIMEOUT):
        flood = True
        timeout = (FLOOD_TIMEOUT - (datetime.now() - request.session['flood_control']).seconds)
    elif not 'flood_control' in request.session or ((datetime.now() - request.session['flood_control']).seconds > FLOOD_TIMEOUT):
        flood = timeout = False
        request.session['flood_control'] = datetime.now()
    else:
        flood = timeout = False

    return flood,timeout

def lastvisit_control(request):
    if request.user.is_authenticated():
        if not "last_visit" in request.session:
            request.session["last_visit"] = datetime.now()
        if not "read_topic_set" in request.session:
            request.session["read_topic_set"] = set()
        if not "read_forum_dict" in request.session:
            request.session["read_forum_dict"] = {}

@login_required
def delete_post(request,forum_slug,topic_id, post_id):
    """ The delete part should be controlled better !"""
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    post = get_object_or_404(Post, pk=post_id)

    if not request.user.has_perm('forum.delete_post'):
        #that one is wrong of course it can return more than one query ...
        #post_user=get_object_or_404(Post,author =request.user)
        user=get_object_or_404(User, username=request.user.username)
        post_user=user.post_set.filter(id=post_id)

        if not post_user:
            return HttpResponse("That is a Wrong way my friend :) ")

    if forum.locked or topic.locked:
        return HttpResponse("Forum or topic is locked")

    if request.method == 'POST':
        post.delete()

    return HttpResponseRedirect(topic.get_absolute_url())
