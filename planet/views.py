#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import render_to_response
from oi.st.models import FS, Game, News, Package, ScreenShot, Tag
from oi.flatpages.models import FlatPage

def home(request):
    news = News.objects.all().order_by('-date')[:4]
    return render_to_response('home.html', locals())

def fs_main(request):
    fs_all = FS.objects.all()
    return render_to_response('fs_main.html', locals())

def fs_detail(request, sef_title):
    fs = FS.objects.get(sef_title=sef_title)
    tags = fs.tags.all()
    return render_to_response('fs_detail.html', locals())

def fs_printable(request, sef_title):
    fs = FS.objects.get(sef_title=sef_title)
    return render_to_response('fs_printable.html', locals())

def game_main(request):
    game_all = Game.objects.all()
    return render_to_response('game_main.html', locals())

def game_detail(request, sef_title):
    game = Game.objects.get(sef_title=sef_title)
    tags = game.tags.all()
    return render_to_response('game_detail.html', locals())

def game_printable(request, sef_title):
    game = Game.objects.get(sef_title=sef_title)
    return render_to_response('game_printable.html', locals())

def news_main(request):
    news = News.objects.all().order_by('-date')[:4]
    return render_to_response('news_main.html', locals())

def news_detail(request, sef_title):
    news = News.objects.get(sef_title=sef_title)
    tags = news.tags.all()
    return render_to_response('news_detail.html', locals())

def news_printable(request, sef_title):
    news = News.objects.get(sef_title=sef_title)
    return render_to_response('news_printable.html', locals())

def pkg_main(request):
    packages = Package.objects.all()
    packages_by_rating = Package.objects.all().order_by('-point')[:10]
    for pkg in packages_by_rating:
        pkg.point = int(round((pkg.point+1)/2))
    return render_to_response('package_main.html', locals())

def pkg_detail(request, name):
    package = Package.objects.get(name=name)
    tags = package.tags.all()
    licenses = package.license.all()
    sss = package.ss.all()
    return render_to_response('package_detail.html', locals())

def pkg_printable(request, name):
    package = Package.objects.get(name=name)
    return render_to_response('package_printable.html', locals())

def tag_main(request):
    tags = Tag.objects.all()
    return render_to_response('tag_main.html', locals())

def tag_detail(request, tag):
    news = News.objects.filter(tags__name__contains=tag)
    packages = Package.objects.filter(tags__name__contains=tag)
    games = Game.objects.filter(tags__name__contains=tag)
    fs = FS.objects.filter(tags__name__contains=tag)
    flatpages = FlatPage.objects.filter(tags__name__contains=tag)
    return render_to_response('tag_detail.html', locals())