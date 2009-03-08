#!/usr/bin/python
# -*- coding: utf-8 -*-

from oi.ezine.models import Ezine
from oi.st.wrappers import render_response

def list(request):
    ezines = Ezine.objects.all().order_by("-id")
    return render_response(request, "list.html", locals())

def detail(request, id):
    ezines = Ezine.objects.filter(pk=id)
    return render_response(request, "list.html", locals())
