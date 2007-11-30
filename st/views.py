#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import sha, datetime, random
from os import path

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from oi.settings import WEB_URL, NEWS_IN_HOMEPAGE, PACKAGES_IN_HOMEPAGE, GAMES_IN_HOMEPAGE, FS_IN_HOMEPAGE, HOWTOS_IN_HOMEPAGE

from oi.st.forms import SearchForm

from oi.st.models import *
from oi.st.wrappers import render_response
from oi.flatpages.models import FlatPage

def home(request):
    news = News.objects.filter(status=1).order_by('-update')[:NEWS_IN_HOMEPAGE]
    packages = Package.objects.filter(status=1).order_by('-update')[:PACKAGES_IN_HOMEPAGE]
    games = Game.objects.filter(status=1).order_by('-update')[:GAMES_IN_HOMEPAGE]
    fss = FS.objects.filter(status=1).order_by('-update')[:FS_IN_HOMEPAGE]
    howtos = HowTo.objects.filter(status=1).order_by('-update')[:HOWTOS_IN_HOMEPAGE]
    return render_response(request, 'home.html', locals())

def fs_detail(request, slug):
    fs = get_object_or_404(FS, slug=slug)
    tags = fs.tags.all()
    videos = fs.videos.all()
    return render_response(request, 'fs/fs_detail.html', locals())

def fs_printable(request, slug):
    fs = get_object_or_404(FS, slug=slug)
    return render_response(request, 'fs/fs_printable.html', locals())

def howto_detail(request, slug):
    howto = get_object_or_404(HowTo, slug=slug)
    tags = howto.tags.all()
    videos = howto.videos.all()
    return render_response(request, 'howto/howto_detail.html', locals())

def howto_printable(request, slug):
    howto = get_object_or_404(HowTo, slug=slug)
    return render_response(request, 'howto/howto_printable.html', locals())

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    tags = game.tags.all()
    videos = game.videos.all()
    for video in videos:
        video.name = path.splitext(video.file)[0].split('/')[2]
    licenses = game.license.all()
    game.avg = ((game.gameplay+game.graphics+game.sound+game.scenario+game.atmosphere)/5.0)
    return render_response(request, 'game/game_detail.html', locals())

def game_printable(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render_response(request, 'game/game_printable.html', locals())

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    tags = news.tags.all()
    return render_response(request, 'news/news_detail.html', locals())

def news_printable(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render_response(request, 'news/news_printable.html', locals())

def pkg_detail(request, slug):
    package = get_object_or_404(Package, slug=slug)
    tags = package.tags.all()
    videos = package.videos.all()
    for video in videos:
        video.name = path.splitext(video.file)[0].split('/')[2]
    licenses = package.license.all()
    sss = package.ss.all()
    return render_response(request, 'package/package_detail.html', locals())

def pkg_printable(request, slug):
    package = get_object_or_404(Package, slug=slug)
    return render_response(request, 'package/package_printable.html', locals())

def tag_detail(request, tag):
    try:
        news = News.objects.filter(tags__name__exact=tag)
        packages = Package.objects.filter(tags__name__exact=tag)
        games = Game.objects.filter(tags__name__exact=tag)
        fs = FS.objects.filter(tags__name__exact=tag)
        howto = HowTo.objects.filter(tags__name__exact=tag)
        flatpages = FlatPage.objects.filter(tags__name__exact=tag)
    except Tag.DoesNotExist:
        raise Http404
    return render_response(request, 'tag/tag_detail.html', locals())

def download(request):
    version = PardusVersion.objects.filter(status=1).order_by('-number')[:1][0]
    install_mirrors = PardusMirror.objects.filter(status=1, type=1).order_by('order')
    live_mirrors = PardusMirror.objects.filter(status=1, type=2).order_by('order')
    return render_response(request, 'download/download.html', locals())

def download_detail_releasenotes(request, version):
    releasenote = get_object_or_404(PardusVersion, number=version).releasenote
    return render_response(request, 'download/download_relnotes.html', locals())

def videobox(request, video):
    vid = get_object_or_404(Video, file=("upload/video/%s.flv" % video))
    web_url = WEB_URL
    return render_response(request, 'videobox.html', locals())

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST.copy())
        if form.is_valid():
            term = form.cleaned_data['term']

            searched = True
            tags = Tag.objects.filter(name__icontains=term).order_by('name')
            news = News.objects.filter(tags__name__icontains=term).order_by('-update')
            packages = Package.objects.filter(tags__name__icontains=term).order_by('-update')
            games = Game.objects.filter(tags__name__icontains=term).order_by('-update')
            fs = FS.objects.filter(tags__name__icontains=term).order_by('-update')
            howto = HowTo.objects.filter(tags__name__icontains=term).order_by('-update')
            flatpages = FlatPage.objects.filter(tags__name__icontains=term).order_by('name')
            total = tags.count()
            total += news.count()
            total += packages.count()
            total += games.count()
            total += fs.count()
            total += howto.count()
            total += flatpages.count()

    else:
        pass

    return render_response(request, 'search.html', locals())
