#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from oi.forum.models import *
from oi.settings import SITE_NAME, WEB_URL, SITE_DESC

from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from oi.forum.models import Topic,Post


class RSS(Feed):
    title = SITE_NAME + "Forum"
    link = WEB_URL
    description = SITE_DESC
    title_template = 'forum/feed_title.html'
    description_template = 'forum/feed_description.html'

    def items(self):
        return Post.objects.filter(hidden=0).order_by('-edited')[:10]

class Atom(RSS):
    feed_type = Atom1Feed
    subtitle = RSS.description
    
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
        
        return Topic.objects.get(id=bits[0]) # get the topic thing
        
        
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
        return Post.objects.filter(topic=obj,hidden=0).order_by('-edited')[:10]
        
    def item_link(self, item):
        """ her biri icin """
        if not item:
            raise FeedDoesNotExist
        return WEB_URL+item.get_absolute_url() 
        
    
class Topic_Atom(Topic_Rss):
    feed_type = Atom1Feed
    subtitle = Topic_Rss.description
    


    
