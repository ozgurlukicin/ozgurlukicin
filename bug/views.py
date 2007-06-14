#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import render_to_response
from oi.bug.models import Bug

def main(request):
    bugs = Bug.objects.all()
    return render_to_response('bug/bug_main.html', locals())

def detail(request, id):
    bug = Bug.objects.get(id=id)
    return render_to_response('bug/bug_detail.html', locals())
