#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.sitemaps import ping_google

from oi.forum.models import Forum, Topic, Post
from oi.middleware import threadlocals

def create_forum_topic(article, forum_name):
    if article.id == None:
        # forum topic not created, lets create
        user = get_object_or_404(User, username=threadlocals.get_current_user())
        forum = Forum.objects.filter(name=forum_name).order_by("id")[0]
        topic = Topic(
                forum = forum,
                title = article.title,
                )
        topic.save()

        post = Post(
                topic=topic,
                author=user,
                text=article.text,
                ip=threadlocals.get_current_ip(),
                hidden=not article.status,
                )
        post.save()

        topic.topic_latest_post = post
        topic.posts = 1
        topic.hidden = not article.status
        topic.topic_latest_post = post
        topic.forum.posts += 1
        topic.forum.topics += 1
        if article.status:
            topic.forum.forum_latest_post = post
        topic.forum.save()
        topic.save()
        article.topic = topic
    else:
        # this is modified, let's update the forum topic
        topic = article.topic
        topic.tags.clear()
        for tag in article.tags.all():
            topic.tags.add(tag)

        topic.hidden = not article.status
        topic.locked = not article.status
        topic.title = article.title
        topic.save()

        post = topic.post_set.order_by("created")[0]
        post.text = article.text
        post.hidden = not article.status
        post.created = post.edited = article.update
        post.save()
    if article.status:
        try:
            ping_google()
        except:
            pass
