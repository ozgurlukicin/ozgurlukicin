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
#    ideas = Idea.objects.filter(is_hidden=False)
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
        if filter_slug == 'bugun':
            ideas = ideas.filter(submitted_date__gt=datetime.datetime.now()-datetime.timedelta(1))
        elif filter_slug == 'buhafta':
            ideas = ideas.filter(submitted_date__gt=datetime.datetime.now()-datetime.timedelta(7))
        elif filter_slug == 'buay':
            ideas = ideas.filter(submitted_date__gt=datetime.datetime.now()-datetime.timedelta(30))
        elif filter_slug == 'tumzamanlar':
            ideas = ideas
    elif field == 'son':
        if filter_slug =='yorumlar':
            comments = Comment.object.order_by("submitted_date")
            ideas = Idea.objects.all()
        elif filter_slug == 'eklenen':
            ideas = ideas.order_by("-submitted_date")
    elif field == 'favori' and filter_slug == 'fikirler':
        favorites = Favorite.objects.filter(user=request.user.id)
        ideas = []
        i = 0
        for idea_id in favorites:
            ideas.append(favorites[i].idea)
            i += 1
    else:
        ideas = ideas.filter()
    categories = Category.objects.all()
    if request.user.is_authenticated():
            for idea in ideas:
                try:
                    f = Favorite.objects.get(user=request.user.id, idea=idea.id)
                    idea.is_favorited = True
                except ObjectDoesNotExist:
                    idea.is_favorited = False
                try:
                    v = Vote.objects.get(user=request.user.id, idea=idea.id)
                    idea.is_voted = True
                except ObjectDoesNotExist:
                    idea.is_voted = False

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
        idea.is_favorited = True
    except ObjectDoesNotExist:
        idea.is_favorited = False
    try:
        v = Vote.objects.get(user=request.user, idea=idea)
        idea.is_voted = True
    except ObjectDoesNotExist:
        idea.is_voted = False

    if request.user.is_authenticated():
        auth = True
    commentform = CommentForm()
    statusform = Status.objects.all()
    duplicates = Idea.objects.filter(duplicate=idea)
    duplicate_of = idea.duplicate
    return render_response(request, "idea_detail.html", locals())

def add(request):
    if request.method == 'POST':
        form = NewIdeaForm(request.POST, request.FILES)
        if form.is_valid():
#            handle_uploaded_file(request.FILES['file'])
            newidea = Idea(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                submitter=request.user,
                category = form.cleaned_data['category'],
                related_to = form.cleaned_data['related_to'],
                forum_url = form.cleaned_data['forum_url'],
                bug_numbers = form.cleaned_data['bug_numbers'],
                status=Status.objects.all()[0]
                )
            newidea.save()
            for tag in form.cleaned_data['tags']:
                tag=Tag.objects.get(name=tag)
                newidea.tags.add(tag)
            idea_added = True


            return HttpResponseRedirect(newidea.get_absolute_url())
    else:
        form = NewIdeaForm(auto_id=True)

    return render_response(request, "idea_add_form.html", locals())


def vote_idea(request, idea_id, vote):
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
    return HttpResponse(str(idea.vote_count))

def delete_vote(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    try:
        vote = Vote.objects.get(user=request.user, idea=idea_id)
        if vote.vote == 1:
            idea.vote_count -= 1
        elif vote.vote == 0:
            idea.vote_count += 1
        vote.delete()
        idea.save()
        return HttpResponse(str(idea.vote_count))
    except ObjectDoesNotExist:
        return HttpResponse(str(idea.vote_count))

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

def duplicate(request, idea_id, duplicate_id):
    try:
        idea = Idea.objects.get(pk=idea_id)
        idea_duplicate = Idea.objects.get(pk=duplicate_id)
        idea_duplicate.vote_count += idea.vote_count
        idea_duplicate.is_duplicate = True
        idea_duplicate.save()
        idea.duplicate = idea_duplicate
        idea.save()
        return HttpResponse("OK")
    except ObjectDoesNotExist:
        return HttpResponse("YOK")

def change_status(request, idea_id, new_status):
    idea = Idea.objects.get(pk=idea_id)
    idea.status_id = new_status
    idea.save()
    return HttpResponse("OK")
