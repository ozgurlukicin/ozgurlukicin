#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.auth.decorators import permission_required

from oi.editor.forms import ContributedNewsForm
from oi.st.wrappers import render_response

@permission_required('editor.change_contributednews', login_url="/kullanici/giris/")
def create_contributednews(request):
    form = ContributedNewsForm()

@permission_required('editor.create_contributednews', login_url="/kullanici/giris/")
def change_contributednews(request):
    form = ContributedNewsForm()

@permission_required('editor.change_contributednews', login_url="/kullanici/giris/")
def list_articles(request):
    "List the news contributed by this user"
    news = ContributedNews.objects.filter(user=request.user, news__status=False)
    return render_response(request, "editor/list.html", {"news":news})
