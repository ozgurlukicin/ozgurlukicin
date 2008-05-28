#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 ArtIstanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from oi.tema.models import Category, ThemeItem, File, ScreenShot, Vote, Comment
from oi.tema.forms import ThemeItemForm
from oi.tema.settings import THEME_ITEM_PER_PAGE
from oi.forum.views import flood_control

from django.views.generic.list_detail import object_list
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

def list_items(request, sort_by):
    "List approved theme items"

    if sort_by == "begenilen":
        themeItems=ThemeItem.objects.filter(approved=True).order_by("-download_count")
    elif sort_by == "indirilen":
        themeItems=ThemeItem.objects.filter(approved=True).order_by("-rating")
    else:
        themeItems=ThemeItem.objects.filter(approved=True).order_by("-edit_date")

    params={
            "queryset": themeItems,
            "paginate_by": THEME_ITEM_PER_PAGE,
            "template_name": "tema/main.html",
            }
    return object_list(request, **params)


def list_category(request, category):
    "List theme items by category"

    category = get_object_or_404(Category, slug=category)
    themeItems = Category.themeitem_set.filter(approved=True)

    params={
            'queryset': themeItems,
            'paginate_by': THEME_ITEM_PER_PAGE,
            'template_name': 'tema/main.html',
            }
    return object_list(request,**params)


def themeitem_detail(request, item_id):
    theme_item = get_object_or_404(ThemeItem, pk=item_id)
    if not theme_item.approved and not request.user == theme_item.author:
        return render_to_response("404.html")

    return render_to_response('tema/themeitem_detail.html', locals())


def list_user(request, username):
    "Theme items of a user"
    user = get_object_or_404(User, username=username)
    themeItems = user.themeitem_set.filter(approved=True)

    params={
            'queryset': themeItems,
            'paginate_by': THEME_ITEM_PER_PAGE,
            'template_name': 'tema/main.html',
            }

    return object_list(request, **params)


@login_required
def vote(request, item_id, rating):
    """
    Vote a theme item.
    If user has already voted, then existing vote should be changed
    """
    theme_item = get_object_or_404(ThemeItem, pk=item_id)

    try:
        vote = Vote.objects.get(theme_item=item_id, user=request.user.id)
        #TODO:vote.setRating(rating)
    except ObjectDoesNotExist:
        vote = Vote(theme_item=item, user=request.user)
        #TODO:vote.setRating(rating)
        vote.save()

    return item_detail(request, item_id)

@login_required
def add_theme_item(request):
    if request.method == "POST":
        form = ThemeItemForm(request.POST.copy())
        flood, timeout = flood_control(request)

        if form.is_valid() and not flood:
            item = ThemeItem(
                    name = form.cleaned_data["name"],
                    category = form.cleaned_data["category"],
                    license = form.cleaned_data["license"],
                    description = form.cleaned_data["description"],
                    changelog = form.cleaned_data["changelog"],
                    comment_enabled = form.cleaned_data["comment_enabled"],

                    author = request.user,
                    )
            item.save()
            return themeitem_detail(request, item.id)
    else:
        form = ThemeItemForm()
    return render_to_response("tema/themeitem_create.html", locals())
