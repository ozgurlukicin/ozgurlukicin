#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 ArtIstanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from oi.forum.views import flood_control
from oi.st.wrappers import render_response
from oi.tema.models import ParentCategory, SubCategory, ThemeItem, File, ScreenShot, Vote, Comment
from oi.tema.forms import ThemeItemForm
from oi.tema.settings import THEME_ITEM_PER_PAGE

from django.views.generic.list_detail import object_list
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

def themeitem_list(request, parentcategory, subcategory, order_by):
    "List approved theme items"
    #first we take approved items
    themeItems=ThemeItem.objects.filter(approved=True)

    #filter by parent category if no subcategory is selected
    if parentcategory != "tum-kategoriler":
        parentcategory = get_object_or_404(ParentCategory, slug=parentcategory)
        themeItems = themeItems.filter(parentcategory=parentcategory)
        parentcategory = parentcategory.slug

    #filter by subcategory
    if subcategory != "tumu":
        subcategory = get_object_or_404(SubCategory, slug=subcategory)
        themeItems = themeItems.filter(category=subcategory)
        subcategory = subcategory.slug

    #order_by
    if order_by == "tarih":
        themeItems = themeItems.order_by("-edit_date")
    elif order_by == "indirilme":
        themeItems = themeItems.order_by("-rating")
    elif order_by == "puan":
        themeItems = themeItems.order_by("-download_count")
    else:# order_by == "alfabe"
        themeItems = themeItems.order_by("name")

    params = {
            "queryset": themeItems,
            "paginate_by": THEME_ITEM_PER_PAGE,
            "extra_context": {
                "order_by": order_by,
                "parentcategory": parentcategory,
                "subcategory": subcategory,
                "categories": ParentCategory.objects.all(),
                },
            }
    return object_list(request, **params)


def themeitem_detail(request, item_id):
    object = get_object_or_404(ThemeItem, pk=item_id)
    if not object.approved and not request.user == object.author:
        return render_response(request, "404.html")

    return render_response(request, 'tema/themeitem_detail.html', locals())


def list_user(request, username):
    "Theme items of a user"
    user = get_object_or_404(User, username=username)
    themeItems = user.themeitem_set.filter(approved=True)

    params={
            'queryset': themeItems,
            'paginate_by': THEME_ITEM_PER_PAGE,
            }
    return object_list(request, **params)


@login_required
def vote(request, item_id, rating):
    """
    Vote a theme item.
    If user has already voted, then existing vote should be changed
    """
    themeitem = get_object_or_404(ThemeItem, pk=item_id)
    rating = int(rating) * 25

    try:
        vote = Vote.objects.get(theme_item=themeitem, user=request.user.id)
        vote.rating = rating
        vote.save()

    except ObjectDoesNotExist:
        vote = Vote(theme_item=themeitem, user=request.user)
        vote.save()

    # Update rating of the item. This can be faster but this way is more convenient
    voteCount = Vote.objects.filter(theme_item=themeitem).count()
    rating = 0
    for vote in Vote.objects.filter(theme_item=themeitem):
        rating += vote.rating
    themeitem.rating = rating / voteCount
    themeitem.save()

    return themeitem_detail(request, item_id)


@login_required
def themeitem_create(request):
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
            item.parentcategory = item.category.parent
            item.save()
            return themeitem_detail(request, item.id)
    else:
        form = ThemeItemForm()
    return render_response(request, "tema/themeitem_create.html", locals())
