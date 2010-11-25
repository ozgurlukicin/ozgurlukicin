#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from oi.settings import SITE_NAME, WEB_URL, SITE_DESC

from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from oi.forum.models import Forum,Topic,Post
from oi.st.tags import Tag


class RSS(Feed):
    title = SITE_NAME + "Forum"
    link = WEB_URL
    description = SITE_DESC
    title_template = 'forum/feed_title.html'
    description_template = 'forum/feed_description.html'

    def items(self):
        objects = Post.objects.filter(hidden=0, topic__forum__is_published=True, topic__forum__hidden=False).order_by('-created')[:120]
        for post in objects:
            post.title = post.topic.title
        return objects

    def item_pubdate(self, item):
        return item.created

    def item_author_name(self, item):
        return item.author

    def item_categories(self, item):
        return [tag.name for tag in item.topic.tags.all()]

class Atom(RSS):
    feed_type = Atom1Feed
    subtitle = RSS.description

class Forum_Rss(RSS):
    def get_object(self, bits):
        return Forum.objects.get(slug=bits[0])

    def items(self, obj):
        objects = Post.objects.filter(hidden=False, topic__forum=obj, topic__forum__hidden=False).order_by('-created')[:40]
        for post in objects:
            post.title = post.topic.title
        return objects

    def title(self, obj):
        return "%s %s forumu" % (SITE_NAME, obj.name)

    def description(self, obj):
        return obj.description

class Forum_Atom(Forum_Rss):
    feed_type = Atom1Feed
    subtitle = Forum_Rss.description

class Topic_Rss(Feed):
    """ Acilan forumlara gore"""
    #author_link = WEB_URL
    title_template = 'forum/feed_title.html'
    description_template = 'forum/feed_description.html'

    def get_object(self,bits):
        """ The forum object
        (r'^(?P<url>.*)/topic/(?P<topic_id>\d+)/$' for that kind of urls
        """
        if not len(bits)==1:
            raise ObjectDoesNotExist

        return Topic.objects.get(id=bits[0].strip()) # get the topic thing

    def title(self,obj):
        """ Istenilen forumun baslik kismi """
        return SITE_NAME + " Forum Konusu : "+obj.title

    def link(self,obj):
        """ Linkini dondur bir de"""
        if not obj:
            raise FeedDoesNotExist
        return WEB_URL+obj.get_absolute_url()

    def description(self,obj):
        """ Konunun aciklamasi fln"""
        return SITE_DESC

    def items(self,obj):
        """ Istenilen Konular burada olacak"""
        return Post.objects.filter(topic=obj,hidden=0).order_by('-created')[:10]

    def item_link(self, item):
        """ her biri icin """
        if not item:
            raise FeedDoesNotExist
        return WEB_URL+item.get_absolute_url()

class Topic_Atom(Topic_Rss):
    feed_type = Atom1Feed
    subtitle = Topic_Rss.description

class Tag_Rss(Topic_Rss):
    """ Acilan Taglara göre Rss"""

    def get_object(self,bits):
        """ The forum object
        (r'^(?P<url>.*)/topic/(?P<topic_id>\d+)/$' for that kind of urls
        """
        if not len(bits)==1:
            raise ObjectDoesNotExist

        return Tag.objects.get(id=bits[0]) # get the topic thing

    def title(self,obj):
        """ Istenilen tag baslik kismi """
        return SITE_NAME + " Forum Tag sıralaması : "+obj.name

    def items(self,obj):
        """ Istenilen Konular burada olacak"""
        return Topic.objects.filter(tags=obj,hidden=0).order_by('title')[:10]

class Tag_Atom(Tag_Rss):
    """ Bir de atom ayağı """
    feed_type = Atom1Feed
    subtitle = Tag_Rss.description
