#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime

from django.contrib.auth.decorators import permission_required

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
def change_contributednews(request):
    form = ContributedNewsForm()

@permission_required('editor.change_contributednews', login_url="/kullanici/giris/")
def list_articles(request):
    "List the news contributed by this user"
    news = ContributedNews.objects.filter(user=request.user, news__status=False)
    return render_response(request, "editor/list.html", {"news":news})
