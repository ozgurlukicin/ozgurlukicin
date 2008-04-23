#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from oi.st.wrappers import render_response
from oi.forum.views import flood_control
from oi.bug.models import Bug, Comment
from oi.bug.forms import BugForm, FullBugForm, CommentForm

@login_required
def add_bug(request):
    if request.method == "POST":
        form = BugForm(request.POST.copy())
        flood, timeout = flood_control(request)

        if form.is_valid() and not flood:
            bug = Bug(
                title = form.cleaned_data["title"],
                submitter = request.user,
                description = form.cleaned_data["description"],
                priority = form.cleaned_data["priority"],
                assigned_to = User.objects.get(name="akin"),
                )
            bug.save()
            return HttpResponseRedirect(bug.get_absolute_url())
    else:
        form = BugForm(auto_id=True)
    return render_response(request, 'bug/bug_add.html', locals())

@permission_required('bug.change_bug', login_url="/kullanici/giris/")
def change_bug(request, id):
    bug = Bug.objects.get(id=id)
    if request.method == "POST":
        form = FullBugForm(request.POST.copy())
        if form.is_valid():
            bug.title = form.cleaned_data["title"]
            bug.description = form.cleaned_data["description"]
            bug.priority = form.cleaned_data["priority"]
            bug.status = form.cleaned_data["status"]
            bug.assigned_to = form.cleaned_data["assigned_to"]
            bug.save()
    return HttpResponseRedirect(bug.get_absolute_url())

def main(request):
    bugs = Bug.objects.all()
    return render_response(request, 'bug/bug_main.html', locals())

def detail(request, id):
    bug = Bug.objects.get(id=id)
    default_data = {
            "title": bug.title,
            "assigned_to": bug.assigned_to.id,
            "description": bug.description,
            "status": bug.status,
            "priority": bug.priority,
            }
    bugform = FullBugForm(default_data)
    if request.method == "POST" and request.user.is_authenticated():
        form = CommentForm(request.POST.copy())
        flood, timeout = flood_control(request)

        if form.is_valid() and not flood:
            comment = Comment(
                bug = bug,
                author = request.user,
                text = form.cleaned_data["text"],
                )
            comment.save()
    else:
        form = CommentForm()
    return render_response(request, 'bug/bug_detail.html', locals())
