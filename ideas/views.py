#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from oi.st.forms import CommentForm
from oi.st.wrappers import render_response
from oi.ideas.models import Idea, Category, Related
from django.contrib.auth.models import User

def list(request, field="", filter_slug=""):
    ideas = Idea.objects.filter(is_hidden=False).order_by("vote_count")
    if field == 'kategori':
        category_id = get_object_or_404(Category, slug = filter_slug)
        ideas = ideas.filter(category=category_id)
    elif field == 'etiket':
        ideas = ideas.filter(tags__name__exact=filter_slug)
    elif field == 'ilgili':
        related_id = get_object_or_404(Related, name  = filter_slug)
        ideas = ideas.filter(related_to=related_id)

    return render_response(request, "idea_list.html", locals())

def detail(request, slug):
    idea = get_object_or_404(Idea, slug=slug)
    form = CommentForm()

    if request.user.is_authenticated():
        auth = True

    return render_response(request, "idea_detail.html", locals())
