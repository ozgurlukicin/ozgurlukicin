#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime

from django.contrib.auth.decorators import permission_required
from django.views.generic.list_detail import object_list
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from oi.editor.forms import ContributedNewsForm
from oi.editor.models import ContributedNews
from oi.st.wrappers import render_response
from oi.st.models import News
from oi.st.tags import Tag
from oi.editor.settings import ARTICLE_PER_PAGE

@permission_required('editor.add_contributednews', login_url="/kullanici/giris/")
def create_contributednews(request):
    if request.method == "POST":
        form = ContributedNewsForm(request.POST.copy())
        if form.is_valid():
            news = News(
                    title = form.cleaned_data["title"],
                    slug = form.cleaned_data["slug"],
                    image = form.cleaned_data["image"],
                    sum = form.cleaned_data["sum"],
                    text = form.cleaned_data["text"],
                    update = datetime.datetime.now(),
                    author = form.cleaned_data["author"],
                    status = False,
                    )
            news.save()

            # add tags
            for tag in form.cleaned_data["tags"]:
                t=Tag.objects.get(name=tag)
                news.tags.add(t)

            contributedNews = ContributedNews(
                    news = news,
                    contributor = request.user,
                    )
            contributedNews.save()
            return HttpResponseRedirect("/editor/")
        else:
            return render_response(request, "editor/create.html", locals())
    else:
        form = ContributedNewsForm()
        return render_response(request, "editor/create.html", locals())

@permission_required('editor.change_contributednews', login_url="/kullanici/giris/")
def change_contributednews(request, news_id):
    contributedNews = get_object_or_404(ContributedNews, id=news_id)
    if not contributedNews.contributor == request.user:
        return HttpResponse("Bu haber sizin değil!")
    if contributedNews.news.status:
        return HttpResponse("Yayına alınmış haberi düzenleyemezsiniz!")

    if request.method == "POST":
        form = ContributedNewsForm(request.POST.copy())
        if form.is_valid():
            news = contributedNews.news
            news.title = form.cleaned_data["title"]
            news.slug = form.cleaned_data["slug"]
            news.image = form.cleaned_data["image"]
            news.sum = form.cleaned_data["sum"]
            news.text = form.cleaned_data["text"]
            news.update = datetime.datetime.now()
            news.author = form.cleaned_data["author"]
            news.tags.clear()
            for tag in form.cleaned_data["tags"]:
                t=Tag.objects.get(name=tag)
                news.tags.add(t)
            news.save()

            return HttpResponseRedirect(news.get_absolute_url())
        else:
            return render_response(request, "editor/change.html", locals())
    else:
        news = contributedNews.news
        dict = {
                "title": news.title,
                "slug": news.slug,
                "image": news.image,
                "sum": news.sum,
                "text": news.text,
                "tags": [tag.id for tag in news.tags.all()],
                "author": news.author,
                }
        form = ContributedNewsForm(initial=dict)
        return render_response(request, "editor/change.html", locals())

@permission_required('editor.change_contributednews', login_url="/kullanici/giris/")
def list_articles(request):
    "List the news contributed by this user"
    news = ContributedNews.objects.filter(contributor=request.user, news__status=False).order_by("-news__update")
    return object_list(request, news,
            template_name = "editor/list.html",
            template_object_name = "news",
            paginate_by = ARTICLE_PER_PAGE,
            allow_empty = True,
            )
