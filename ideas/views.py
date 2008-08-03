#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from oi.st.forms import CommentForm
from oi.st.wrappers import render_response
from oi.ideas.models import Idea
from django.contrib.auth.models import User

def list(request):
    ideas = Idea.objects.filter(is_hidden=False).order_by("vote_count")
    return render_response(request, "idea_list.html", locals())

def detail(request, slug):
    i = get_object_or_404(Idea, slug=slug)
    form = CommentForm()

    if request.user.is_authenticated():
        auth = True

    return render_response(request, "idea_detail.html", locals())



