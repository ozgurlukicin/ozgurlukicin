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
from django.db.models import Q

from oi.settings import WEB_URL, NEWS_IN_HOMEPAGE, PACKAGES_IN_HOMEPAGE, GAMES_IN_HOMEPAGE, FS_IN_HOMEPAGE, HOWTOS_IN_HOMEPAGE

from oi.st.forms import SearchForm,CommentForm,AdvancedSearchForm

from oi.st.models import *
from oi.st.wrappers import render_response
from oi.flatpages.models import FlatPage

#for comments
from django.contrib.auth.decorators import login_required
from oi.forum.models import Forum,Topic,Post
from oi.forum.views import flood_control
from django.http import HttpResponseRedirect

def robots(request):
    return render_response(request, 'robots.txt')

def home(request):
    news = News.objects.filter(status=True).order_by('-update')[:NEWS_IN_HOMEPAGE]
    packages = Package.objects.filter(status=True).order_by('-update')[:PACKAGES_IN_HOMEPAGE]
    games = Game.objects.filter(status=True).order_by('-update')[:GAMES_IN_HOMEPAGE]
    howtos = HowTo.objects.filter(status=True).order_by('-update')[:HOWTOS_IN_HOMEPAGE]
    return render_response(request, 'home.html', locals())

def fs_detail(request, slug):
    fs = get_object_or_404(FS, slug=slug)
    return render_response(request, 'fs/fs_detail.html', locals())

def fs_printable(request, slug):
    fs = get_object_or_404(FS, slug=slug)
    return render_response(request, 'fs/fs_printable.html', locals())

def howto_detail(request, slug):
    howto = get_object_or_404(HowTo, slug=slug)

    form=CommentForm()

    if request.user.is_authenticated():
        auth=True

    try:
        topic = Topic.objects.filter(title=howto.title)[0]
        comment_count = topic.posts - 1
        comment_url = topic.get_latest_post_url()
    except:
        pass
    return render_response(request, 'howto/howto_detail.html', locals())

def howto_printable(request, slug):
    howto = get_object_or_404(HowTo, slug=slug)
    return render_response(request, 'howto/howto_printable.html', locals())

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    game.avg = ((game.gameplay + game.graphics + game.sound + game.scenario + game.atmosphere)/5.0)

    form=CommentForm()

    if request.user.is_authenticated():
        auth=True

    try:
        topic = Topic.objects.filter(title=game.title)[0]
        comment_count = topic.posts - 1
        comment_url = topic.get_latest_post_url()
    except:
        pass

    return render_response(request, 'game/game_detail.html', locals())

def game_printable(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render_response(request, 'game/game_printable.html', locals())

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    form=CommentForm()

    if request.user.is_authenticated():
        auth=True

    try:
        topic = Topic.objects.filter(title=news.title)[0]
        comment_count = topic.posts - 1
        comment_url = topic.get_latest_post_url()
    except:
        pass
    return render_response(request, 'news/news_detail.html', locals())

def news_printable(request, slug):
    news = get_object_or_404(News, slug=slug)

    return render_response(request, 'news/news_printable.html', locals())

def pkg_detail(request, slug):
    package = get_object_or_404(Package, slug=slug)

    form=CommentForm()

    if request.user.is_authenticated():
        auth=True

    # we need to handle page titles that changed after creating
    try:
        topic = Topic.objects.filter(title=package.title)[0]
        comment_count = topic.posts - 1
        comment_url = topic.get_latest_post_url()
    except:
        pass

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
        topic=Topic.objects.filter(tags__name__exact=tag)

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

def advanced_search(request):
    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST.copy())
        if form.is_valid():
            term = form.cleaned_data['term']
            search_in = int(form.cleaned_data['search_in'])
            depth = int(form.cleaned_data['depth'])

            tags = Tag.objects.filter(name__icontains=term)

            if depth == 0:
                if search_in != 1:
                    topics = Topic.objects.filter(title__icontains=term)[:50]
                if search_in != 0:
                    news = News.objects.filter(title__icontains=term).order_by('-update')
                    packages = Package.objects.filter(title__icontains=term).order_by('-update')
                    games = Game.objects.filter(title__icontains=term).order_by('-update')
                    fs = FS.objects.filter(title__icontains=term).order_by('-update')
                    howto = HowTo.objects.filter(title__icontains=term).order_by('-update')
                    flatpages = FlatPage.objects.filter(title__icontains=term)
            else:
                if search_in != 1:
                    posts = Post.objects.filter(text__icontains=term).order_by("-created")[:50]
                if search_in != 0:
                    news = News.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).order_by('-update')
                    packages = Package.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).order_by('-update')
                    games = Game.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).order_by('-update')
                    fs = FS.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).order_by('-update')
                    howto = HowTo.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).order_by('-update')
                    flatpages = FlatPage.objects.filter(Q(title__icontains=term)|Q(text__icontains=term))
            searched = True
    else:
        form = AdvancedSearchForm()
    return render_response(request, 'advancedsearch.html', locals())

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
            flatpages = FlatPage.objects.filter(tags__name__icontains=term).order_by('title')
            #for forum also
            topic=Topic.objects.filter(tags__name__icontains=term).order_by('title')

            total = tags.count()
            total += news.count()
            total += packages.count()
            total += games.count()
            total += fs.count()
            total += howto.count()
            total += flatpages.count()
            total += topic.count()

    return render_response(request, 'search.html', locals())

@login_required
def comment_news(request,slug):
    """ When someone comments it is adde to forum (check for flooding also !)...
    validate the html tags all for now...(may change!)
    """
    news = get_object_or_404(News, slug=slug)
    #news = News.objects.filter(id=id)

    if request.method== 'POST':
        new_data = request.POST.copy()
        form=CommentForm(new_data)

        #flood control
        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            t=Topic.objects.filter(title=news.title)
            if not t:
                tags = news.tags.all()
                return render_response(request,'news/news_detail.html',{'news':news,'tags':tags,'form':form,'auth':True})

            if t[0].locked:
                errorMessage = 'Konu kilitli olduğu için yorum gönderemezsiniz.'
                return render_response(request, 'forum/forum_error.html', {'message': errorMessage})

            post = Post(topic=t[0],
                        author=request.user,
                        text=form.cleaned_data['yorum'])
            try:
                post.save()
            except Exception:
                render_to_response('db_error.html')

            return HttpResponseRedirect(post.get_absolute_url())
        else:
            #hata mesaji gonder
            tags = news.tags.all()
            return render_response(request,'news/news_detail.html',{'news':news,'tags':tags,'form':form,'auth':True})

    form = CommentForm()
    tags = news.tags.all()
    return render_response(request,'news/news_detail.html',{'news':news,'tags':tags,'form':form,'auth':True})

    #do something here


@login_required
def comment_howto(request,slug):
    """ When someone comments it is adde to forum (check for flooding also !)...
    validate the html tags all for now...(may change!)
    """
    howto = get_object_or_404(HowTo, slug=slug)
    #news = News.objects.filter(id=id)

    if request.method== 'POST':
        new_data = request.POST.copy()
        form=CommentForm(new_data)

        #flood control
        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            t=Topic.objects.filter(title=howto.title)
            if not t:
                tags = howto.tags.all()
                return render_response(request,'howto/howto_detail.html',{'howto':howto,'tags':tags,'form':form,'auth':True})

            if t[0].locked:
                errorMessage = 'Konu kilitli olduğu için yorum gönderemezsiniz.'
                return render_response(request, 'forum/forum_error.html', {'message': errorMessage})

            post = Post(topic=t[0],
                        author=request.user,
                        text=form.cleaned_data['yorum'])
            try:
                post.save()
            except Exception:
                render_to_response('db_error.html')

            return HttpResponseRedirect(post.get_absolute_url())
        else:
            #hata mesaji gonder
            tags = howto.tags.all()
            return render_response(request,'howto/howto_detail.html',{'howto':howto,'tags':tags,'form':form,'auth':True})

    form=CommentForm()
    tags = howto.tags.all()
    return render_response(request,'howto/howto_detail.html',{'howto':howto,'tags':tags,'form':form,'auth':True})

    #do something here

@login_required
def comment_game(request,slug):
    """ When someone comments it is adde to forum (check for flooding also !)...
    validate the html tags all for now...(may change!)
    """
    game = get_object_or_404(Game, slug=slug)
    #news = News.objects.filter(id=id)

    if request.method== 'POST':
        new_data = request.POST.copy()
        form=CommentForm(new_data)

        #flood control
        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            t=Topic.objects.filter(title=game.title)
            if not t:
                tags = game.tags.all()
                return render_response(request,'game/game_detail.html',{'game':game,'tags':tags,'form':form,'auth':True})

            if t[0].locked:
                errorMessage = 'Konu kilitli olduğu için yorum gönderemezsiniz.'
                return render_response(request, 'forum/forum_error.html', {'message': errorMessage})

            post = Post(topic=t[0],
                        author=request.user,
                        text=form.cleaned_data['yorum'])
            try:
                post.save()
            except Exception:
                render_to_response('db_error.html')

            return HttpResponseRedirect(post.get_absolute_url())
        else:
            #hata mesaji gonder
            tags = game.tags.all()
            return render_response(request,'game/game_detail.html',{'game':game,'tags':tags,'form':form,'auth':True})

    form=CommentForm()
    tags = game.tags.all()
    return render_response(request,'game/game_detail.html',{'game':game,'tags':tags,'form':form,'auth':True})

    #do something here

@login_required
def comment_package(request,slug):
    """ When someone comments it is adde to forum (check for flooding also !)...
    validate the html tags all for now...(may change!)
    """
    package = get_object_or_404(Package, slug=slug)
    #news = News.objects.filter(id=id)

    if request.method== 'POST':
        new_data = request.POST.copy()
        form=CommentForm(new_data)

        #flood control
        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            t=Topic.objects.filter(title=package.title)
            if not t:
                tags = package.tags.all()
                return render_response(request,'package/package_detail.html',{'package':package,'tags':tags,'form':form,'auth':True})

            if t[0].locked:
                errorMessage = 'Konu kilitli olduğu için yorum gönderemezsiniz.'
                return render_response(request, 'forum/forum_error.html', {'message': errorMessage})

            post = Post(topic=t[0],
                        author=request.user,
                        text=form.cleaned_data['yorum'])
            try:
                post.save()
            except Exception:
                render_to_response('db_error.html')

            return HttpResponseRedirect(post.get_absolute_url())
        else:
            #hata mesaji gonder
            tags = package.tags.all()
            return render_response(request,'package/package_detail.html',{'package':package,'tags':tags,'form':form,'auth':True})

    form=CommentForm()
    tags = package.tags.all()
    return render_response(request,'package/package_detail.html',{'package':package,'tags':tags,'form':form,'auth':True})

    #do something here
