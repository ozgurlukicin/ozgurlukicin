#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007, 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

from oi.settings import WEB_URL, NEWS_IN_HOMEPAGE, PACKAGES_IN_HOMEPAGE, GAMES_IN_HOMEPAGE, FS_IN_HOMEPAGE, HOWTOS_IN_HOMEPAGE

from oi.st.forms import SearchForm,AdvancedSearchForm

from oi.st.models import News, Package, Game, HowTo, Workshop, FS, PardusVersion, PardusMirror
from oi.st.tags import Tag
from oi.st.wrappers import render_response
from oi.flatpages.models import FlatPage
from oi.seminar.models import Seminar
from oi.ideas.models import Idea

#for comments
from django.contrib.auth.decorators import login_required
from oi.forum.models import Forum,Topic,Post
from oi.forum.views import flood_control
from oi.forum.forms import PostForm
from django.http import HttpResponseRedirect

def robots(request):
    return render_response(request, 'robots.txt')

def home(request):
    news = News.objects.filter(status=True).order_by('-update')[:NEWS_IN_HOMEPAGE]
    packages = Package.objects.filter(status=True).order_by('-update')[:PACKAGES_IN_HOMEPAGE]
    games = Game.objects.filter(status=True).order_by('-update')[:GAMES_IN_HOMEPAGE]
    howtos = HowTo.objects.filter(status=True).order_by('-update')[:HOWTOS_IN_HOMEPAGE]
    seminar = Seminar.objects.filter(status=True).order_by('start_date')
    return render_response(request, 'home.html', locals())

def fs_detail(request, slug):
    fs = get_object_or_404(FS, slug=slug)
    return render_response(request, 'fs/fs_detail.html', locals())

def fs_printable(request, slug):
    fs = get_object_or_404(FS, slug=slug)
    return render_response(request, 'fs/fs_printable.html', locals())

def howto_detail(request, slug):
    howto = get_object_or_404(HowTo, slug=slug)
    if howto.logo:
        related_howtos = howto.logo.howto_set.filter(status=True).exclude(id=howto.id)
    form=PostForm()
    return render_response(request, 'howto/howto_detail.html', locals())

def howto_printable(request, slug):
    howto = get_object_or_404(HowTo, slug=slug)
    return render_response(request, 'howto/howto_printable.html', locals())

def workshop_detail(request, slug):
    workshop = get_object_or_404(Workshop, slug=slug)
    if workshop.logo:
        related_workshops = workshop.logo.workshop_set.filter(status=True).exclude(id=workshop.id)
    form = PostForm()
    return render_response(request, 'workshop/workshop_detail.html', locals())

def workshop_printable(request, slug):
    workshop = get_object_or_404(Workshop, slug=slug)
    return render_response(request, 'workshop/workshop_printable.html', locals())

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    game.avg = ((game.gameplay + game.graphics + game.sound + game.scenario + game.atmosphere)/5.0)
    game.gameplay_range = range(0, game.gameplay)
    game.gameplay_range_empty = range(0, 10 - game.gameplay)
    game.graphics_range = range(0, game.graphics)
    game.graphics_range_empty = range(0, 10 - game.graphics)
    game.sound_range = range(0, game.sound)
    game.sound_range_empty = range(0, 10 - game.sound)
    game.scenario_range = range(0, game.scenario)
    game.scenario_range_empty = range(0, 10 - game.scenario)
    game.atmosphere_range = range(0, game.atmosphere)
    game.atmosphere_range_empty = range(0, 10 - game.atmosphere)
    form=PostForm()
    return render_response(request, 'game/game_detail.html', locals())

def game_printable(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render_response(request, 'game/game_printable.html', locals())

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    if not news.status and not request.user.has_perm("editor.change_contributednews"):
        return render_response(request, "404.html")
    form=PostForm()
    return render_response(request, 'news/news_detail.html', locals())

def news_printable(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render_response(request, 'news/news_printable.html', locals())

def pkg_detail(request, slug):
    package = get_object_or_404(Package, slug=slug)
    form=PostForm()
    return render_response(request, 'package/package_detail.html', locals())

def pkg_printable(request, slug):
    package = get_object_or_404(Package, slug=slug)
    return render_response(request, 'package/package_printable.html', locals())

def tag_detail(request, tag):
    try:
        news = News.objects.filter(tags__name__exact=tag, status=True)[:100]
        packages = Package.objects.filter(tags__name__exact=tag, status=True)[:100]
        games = Game.objects.filter(tags__name__exact=tag, status=True)[:100]
        fs = FS.objects.filter(tags__name__exact=tag, status=True)[:100]
        howto = HowTo.objects.filter(tags__name__exact=tag, status=True)[:100]
        flatpages = FlatPage.objects.filter(tags__name__exact=tag)[:100]
        topic=Topic.objects.filter(tags__name__exact=tag, hidden=False).order_by("-id")[:100]

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

            tags = Tag.objects.filter(name__icontains=term)[:50]

            if depth == 0:
                if search_in == 0 or search_in == 2:
                    topics = Topic.objects.filter(title__icontains=term, hidden=False)[:50]
                if search_in == 3 or search_in == 2:
                    ideas = Idea.objects.filter(title__icontains=term, is_hidden=False).order_by('-vote_count')[:50]
                if search_in == 1 or search_in == 2:
                    news = News.objects.filter(title__icontains=term, status=True).order_by('-update')[:50]
                    packages = Package.objects.filter(title__icontains=term, status=True).order_by('-update')[:50]
                    games = Game.objects.filter(title__icontains=term, status=True).order_by('-update')[:50]
                    fs = FS.objects.filter(title__icontains=term, status=True).order_by('-update')[:50]
                    howto = HowTo.objects.filter(title__icontains=term, status=True).order_by('-update')[:50]
                    workshop = Workshop.objects.filter(title__icontains=term, status=True).order_by('-update')[:50]
                    flatpages = FlatPage.objects.filter(title__icontains=term)[:50]
            else:
                if search_in == 0 or search_in == 2:
                    posts = Post.objects.filter(text__icontains=term, hidden=False).order_by("-created")[:50]
                if search_in == 3 or search_in == 2:
                    ideas = Idea.objects.filter(Q(title__icontains=term)|Q(description__icontains=term)).filter(is_hidden=False).order_by('-vote_count')[:50]
                if search_in == 1 or search_in == 2:
                    news = News.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).filter(status=True).order_by('-update')[:50]
                    packages = Package.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).filter(status=True).order_by('-update')[:50]
                    games = Game.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).filter(status=True).order_by('-update')[:50]
                    fs = FS.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).filter(status=True).order_by('-update')[:50]
                    howto = HowTo.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).filter(status=True).order_by('-update')[:50]
                    workshop = Workshop.objects.filter(Q(title__icontains=term)|Q(text__icontains=term)).filter(status=True).order_by('-update')[:50]
                    flatpages = FlatPage.objects.filter(Q(title__icontains=term)|Q(text__icontains=term))[:50]
            searched = True
    else:
        form = AdvancedSearchForm()
    return render_response(request, 'advancedsearch.html', locals())
