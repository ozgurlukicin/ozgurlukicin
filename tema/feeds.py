#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbulpr
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from oi.tema.models import File,Category
from oi.settings import SITE_NAME, WEB_URL, SITE_DESC

from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class Tema_RSS(Feed):
    title = SITE_NAME + "Temalar"
    link = WEB_URL
    description = SITE_DESC + "Pencere dekorasyonları, duvar kağıtları ve daha fazlası."
    title_template = 'tema/feed_title.html'
    description_template = 'tema/feed_description.html'

    def items(self):
        return File.objects.filter(state=True).order_by("-update")[:10]

class Tema_Atom(Tema_RSS):
    feed_type = Atom1Feed
    subtitle = Tema_RSS.description

###############################################################################
class Category_Tema_Rss(Feed):
    """ Categoriye göre"""

    #author_link = WEB_URL
    title_template = 'forum/feed_title.html'
    description_template = 'forum/feed_description.html'

    def get_object(self,bits):
        """ The forum object
        (r'^(?P<url>.*)/topic/(?P<topic_id>\d+)/$' for that kind of urls
        """
        if not len(bits)==1:
            raise ObjectDoesNotExist

        return Category.objects.get(id=bits[0]) # get the topic thing


    def title(self,obj):
        """ Istenilen forumun baslik kismi """
        return SITE_NAME + " Tema Kategori : "+obj.cat_name

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
        return File.objects.filter(parent_cat=obj,state=True).order_by('-update')[:10]

    def item_link(self, item):
        """ her biri icin """
        if not item:
            raise FeedDoesNotExist
        return WEB_URL+item.get_absolute_url()


class Category_Tema_Atom(Category_Tema_Rss):
    """ Category Atom"""
    feed_type = Atom1Feed
    subtitle = Category_Tema_Rss.description
 ##########################################################################
class User_Tema_Rss(Feed):
    """ Kullaniciya göre rss"""
    title_template = 'forum/feed_title.html'
    description_template = 'forum/feed_description.html'

    def get_object(self,bits):
        """ The forum object
        (r'^(?P<url>.*)/topic/(?P<topic_id>\d+)/$' for that kind of urls
        """
        if not len(bits)==1:
            raise ObjectDoesNotExist

        return User.objects.get(id=bits[0]) # get the topic thing

    def title(self,obj):
        """ Istenilen forumun baslik kismi """
        return SITE_NAME + " Tema Kullanici : "+obj.username

    def description(self,obj):
        """ Konunun aciklamasi fln"""
        return SITE_DESC

    def link(self,obj):
        """ Linkini dondur bir de"""
        if not obj:
            raise FeedDoesNotExist
        return WEB_URL+"/tema/kullanici/"+str(obj.username)+"/"

    def items(self,obj):
        """ Istenilen Konular burada olacak"""
        return File.objects.filter(user=obj,state=True).order_by('-update')[:10]

    def item_link(self, item):
        """ her biri icin """
        if not item:
            raise FeedDoesNotExist
        return WEB_URL+item.get_absolute_url()


class User_Tema_Atom(User_Tema_Rss):
    """ Bu da atom kısmı olsun """
    feed_type = Atom1Feed
    subtitle = User_Tema_Rss.description
