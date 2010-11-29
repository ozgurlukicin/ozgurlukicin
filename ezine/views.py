#!/usr/bin/python
# -*- coding: utf-8 -*-

from oi.ezine.models import Ezine
from oi.st.wrappers import render_response

def list(request):
    ezines = Ezine.objects.filter(is_active=True).order_by("-issue")
    return render_response(request, "list.html", locals())

def detail(request, id):
    ezines = Ezine.objects.filter(issue=id)
    return render_response(request, "list.html", locals())
