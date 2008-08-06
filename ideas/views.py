#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from oi.ideas.forms import *
from oi.st.wrappers import render_response
from oi.ideas.models import Idea, Category, Related, Comment, Status
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
    elif field == 'ekleyen':
        submitter_id = get_object_or_404(User, username = filter_slug)
        ideas = ideas.filter(submitter = submitter_id)

    categories = Category.objects.all()
    absolute_url = "/yenifikir"
    return render_response(request, "idea_list.html", locals())

def detail(request, slug):
    absolute_url = "/yenifikir"
    idea = get_object_or_404(Idea, slug=slug)
    if request.method == 'POST':
        idea = get_object_or_404(Idea, slug=slug)
        form = CommentForm(request.POST.copy())
        if form.is_valid():
            text = form.cleaned_data['text']
            ip = request.META['REMOTE_ADDR']
            comment = Comment(
                idea=idea,
                text=text,
                author = request.user,
                ip=ip
                )
            comment.save()
#            HttpResponseRedirect("%s/%s", (absolute_url, slug))

    comments = Comment.objects.filter(is_hidden=False, idea=idea)
    form = CommentForm()

    if request.user.is_authenticated():
        auth = True
    commentform = CommentForm()
    return render_response(request, "idea_detail.html", locals())

def add(request):
    if request.method == 'POST':
        form = NewIdeaForm(request.POST.copy())
        if form.is_valid():
            status = Status.objects.all()[1]
            newidea = Idea(request.POST, submitter=request.user, status=status)
            newidea.save()
            idea_added = True
    else:
        new_idea_form = NewIdeaForm()
    return render_response(request, "idea_add_form.html", locals())





