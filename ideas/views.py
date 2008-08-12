#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from oi.ideas.forms import *
from oi.st.wrappers import render_response
from oi.ideas.models import Idea, Category, Related, Comment, Status, Tag, Vote, Favorite
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import datetime


def list(request, field="", filter_slug=""):
    ideas = Idea.objects.filter(is_hidden=False).order_by("-vote_count", "-id")
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
    elif field == 'populer':
        if filter_slug == 'buhafta':
            ideas = ideas.filter(submitted_date__gt=datetime.datetime.now()-datetime.timedelta(7))
        elif filter_slug == 'buay':
            ideas = ideas.filter(submitted_date__gt=datetime.datetime.now()-datetime.timedelta(30))
        elif filter_slug == 'tumzamanlar':
            ideas = ideas
    elif field == 'son' and filter_slug =='yorumlar':
        ideas = ideas.filter()
    elif field == 'favori' and filter_slug == 'fikirler':
        favorites = Favorite.objects.filter(user=request.user.id)
        ideas = []
        i = 0
        for idea_id in favorites:
            ideas.append(favorites[i].idea)
            i += 1
    else:
        ideas = ideas.filter(submitted_date__gt=datetime.datetime.now()-datetime.timedelta(1))
    categories = Category.objects.all()
    absolute_url = "/yenifikir"
    return render_response(request, "idea_list.html", locals())

def detail(request, idea_id):
    absolute_url = "/yenifikir"
    idea = get_object_or_404(Idea, pk=idea_id)
    if request.method == 'POST':
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
            return HttpResponseRedirect(idea.get_absolute_url())
    comments = Comment.objects.filter(is_hidden=False, idea=idea)
    form = CommentForm()
    try:
        f = Favorite.objects.get(user=request.user, idea=idea)
        favorited = True
    except ObjectDoesNotExist:
        favorited = False

    if request.user.is_authenticated():
        auth = True
    commentform = CommentForm()
    return render_response(request, "idea_detail.html", locals())

def add(request):
    if request.method == 'POST':
        form = NewIdeaForm(request.POST.copy())
        if form.is_valid():
            newidea = Idea(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                submitter=request.user,
                category = form.cleaned_data['category'],
                related_to = form.cleaned_data['related_to'],
                forum_url = form.cleaned_data['forum_url'],
                bug_numbers = form.cleaned_data['bug_numbers'],
                status=Status.objects.all()[0])
            newidea.save()
            for tag in form.cleaned_data['tags']:
                tag=Tag.objects.get(name=tag)
                newidea.tags.add(tag)

            idea_added = True
    else:
        new_idea_form = NewIdeaForm()
    return render_response(request, "idea_add_form.html", locals())


def vote_idea(request, idea_id, vote):
#    idea = get_object_or_404(Idea, pk=idea_id)
    idea = Idea.objects.get(pk=idea_id)
    try:
        vote = Vote.objects.get(user=request.user.id, idea=idea)
        already_voted = True
    except ObjectDoesNotExist:
        if vote=='1':
            idea.vote_count += 1
        else:
            idea.vote_count -= 1
        idea.save()
        voted = Vote(idea = idea, user=request.user, vote=vote)
        voted.save()
    return render_response(request, "idea_detail.html", locals())

def add_favorite(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    try:
        favorite = Favorite.objects.get(user=request.user, idea=idea)
        favorited = True
    except ObjectDoesNotExist:
        favorite = Favorite(user=request.user, idea=idea)
        favorite.save()
    return HttpResponse("OK")

def del_favorite(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    favorite = Favorite.objects.get(user=request.user, idea=idea_id)
    favorite.delete()
    return HttpResponse("OK")
