#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from oi.st.models import HowTo, News, Game, Package
from oi.forum.models import Forum, Topic
from django.contrib.auth.models import User

def the_filler(instance,u):
    """ The actual filler"""
    if instance._meta.module_name=="howto":
        name="Nasıl"

    elif instance._meta.module_name=="game":
        name="Oyunlar"

    elif instance._meta.module_name=="package":
        name="Paketler"

    elif instance._meta.module_name=="news":
        name="Haberler"

    forum=Forum.objects.filter(name=name)

    if not forum :
        return

    t=Topic.objects.filter(title=instance.title)


    if not t:
        topic = Topic(forum=forum[0],
                                  title=instance.title #or any
                            )
        topic.save()

        post = Post(topic=topic,
                            author=u,
                            text=instance.text,
                            ip="127.0.0.1"
                               )
        post.save()

    else:
        return

    return


def fill_howto(user=None):
    """ Fill the news"""
    howtos=HowTo.objects.all().order_by('update')

    u=User.objects.filter(username=user)

    if not u:
        print "Bu kullanıcı yok"
        return False


    for howto in howtos:
        the_filler(howto,u[0])

    print "howtos added to forum"

def fill_news(user=None):
    """ Fill the news"""
    news=News.objects.all().order_by('update')

    u=User.objects.filter(username=user)

    if not u:
        print "Bu kullanıcı yok"
        return False


    for n in news:
        the_filler(n,u[0])

    print "news added to forum"

def fill_game(user=None):
    """ Fill the news"""
    games=Game.objects.all().order_by('update')

    u=User.objects.filter(username=user)

    if not u:
        print "Bu kullanıcı yok"
        return False


    for game in games:
        the_filler(game,u[0])

    print "games added to forum"


def fill_package(user=None):
    """ Fill the news"""
    packages=Package.objects.all().order_by('update')

    u=User.objects.filter(username=user)

    if not u:
        print "Bu kullanıcı yok"
        return False


    for package in packages:
        the_filler(package,u[0])

    print "packages  added to forum"


def call_all(user=None):
    """ Call them all"""
    fill_howto(user)
    fill_news(user)
    fill_game(user)
    fill_package(user)
