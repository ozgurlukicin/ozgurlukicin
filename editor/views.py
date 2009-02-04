#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404

from oi.editor.forms import ContributedNewsForm
from oi.editor.models import ContributedNews
from oi.st.wrappers import render_response
from oi.st.models import News

@permission_required('editor.change_contributednews', login_url="/kullanici/giris/")
def create_contributednews(request):
    if request.method == 'POST':
        form = ContributedNewsForm(request.POST.copy())
        if form.is_valid():
            news = News(
                    title = form.cleaned_data["title"],
                    slug = form.cleaned_data["slug"],
                    image = form.cleaned_data["image"],
                    sum = form.cleaned_data["sum"],
                    text = form.cleaned_data["text"],
                    tags = form.cleaned_data["tags"],
                    update = datetime.datetime.now(),
                    author = form.cleaned_data["author"],
                    status = False,
                    )
            news.save()
            contributedNews = ContributedNews(
                    news = news,
                    contributor = request.user,
                    )
            contributedNews.save()
            return HttpResponseRedirect(news.get_absolute_url())
        else:
            return render_response(request, "editor/create.html", locals())
    else:
        form = ContributedNewsForm()
        return render_response(request, "editor/create.html", locals())

@permission_required('editor.create_contributednews', login_url="/kullanici/giris/")
def change_contributednews(request, news_id):
    contributedNews = get_object_or_404(ContributedNews, id=news_id)
    if not contributedNews.contributor == request.user:
        return HttpResponse("Bu haber sizin değil!")
    if contributedNews.news.status:
        return HttpResponse("Yayına alınmış haberi düzenleyemezsiniz!")

    if request.method == 'POST':
        form = ContributedNewsForm(request.POST.copy())
        if form.is_valid():
            news = contributedNews.news
            news.title = form.cleaned_data["title"]
            news.slug = form.cleaned_data["slug"]
            news.image = form.cleaned_data["image"]
            news.sum = form.cleaned_data["sum"]
            news.text = form.cleaned_data["text"]
            news.tags = form.cleaned_data["tags"]
            news.update = datetime.datetime.now()
            news.author = form.cleaned_data["author"]
            news.save()
            return HttpResponseRedirect(news.get_absolute_url())
        else:
            return render_response(request, "editor/create.html", locals())
    else:
        form = ContributedNewsForm(initial=dict(contributedNews))
        return render_response(request, "editor/create.html", locals())

@permission_required('editor.change_contributednews', login_url="/kullanici/giris/")
def list_articles(request):
    "List the news contributed by this user"
    news = ContributedNews.objects.filter(contributor=request.user, news__status=False)
    return render_response(request, "editor/list.html", {"news":news})
