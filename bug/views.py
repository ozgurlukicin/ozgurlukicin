#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.auth.decorators import login_required

from oi.st.wrappers import render_response
from oi.bug.models import Bug
from oi.bug.forms import BugForm

@login_required
def add_bug(request):
    form = BugForm(auto_id=True)
    return render_response(request, 'bug/bug_add.html', locals())

def main(request):
    bugs = Bug.objects.all()
    return render_response(request, 'bug/bug_main.html', locals())

def detail(request, id):
    bug = Bug.objects.get(id=id)
    return render_response(request, 'bug/bug_detail.html', locals())
