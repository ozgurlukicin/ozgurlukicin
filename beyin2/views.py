#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.http import HttpResponse
from oi.beyin2.models import Idea
from oi.beyin2.forms import IdeaForm
from oi.st.wrappers import render_response

def main(request):
    idea_list = Idea.objects.all().order_by('-dateSubmitted')[:10]
    return render_response(request,'beyin2/idea_list.html',{'idea_list': idea_list})

def add_new(request):
    form = IdeaForm({'title': '', 'description': '', 'status': '', 'category': ''})

    return render_response(request,'beyin2/idea_new.html',{'form':form,})

