#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from oi.st.wrappers import render_response
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from oi.paste.models import PastedText
from oi.paste.forms import PastedTextForm
from oi.middleware import threadlocals

@login_required
def pastedtext_add(request):
    if request.method == "POST":
        form = PastedTextForm(request.POST.copy())
        if form.is_valid():
            paste = form.save(commit=False)
            paste.author = request.user
            paste.ip = threadlocals.get_current_ip()
            paste.save()
            return HttpResponseRedirect(paste.get_absolute_url())
    else:
        form = PastedTextForm()
    return render_response(request, "paste/pastedtext_add.html", {"form":form})

@permission_required('paste.hide_pastedtext', login_url="/kullanici/giris/")
def pastedtext_toggle_hidden(request, id):
    paste = get_object_or_404(PastedText, id=id)
    if request.method == "POST":
        paste.is_hidden = not paste.is_hidden
        paste.save()
        return HttpResponseRedirect(paste.get_absolute_url())
    return render_response(request, "paste/pastedtext_toggle.html", {"paste":paste})

@login_required
def pastedtext_hide(request, id):
    paste = get_object_or_404(PastedText, id=id)
    if request.user == paste.author:
        if request.method == "POST":
            paste.is_hidden = True
            paste.save()
            return HttpResponseRedirect(paste.get_absolute_url())
        return render_response(request, "paste/pastedtext_toggle.html", {"paste":paste})
    else:
        return HttpResponseRedirect("/kullanici/giris/")


def pastedtext_detail(request, id):
    paste = get_object_or_404(PastedText, id=id)
    return render_response(request, "paste/pastedtext_detail.html", {"paste":paste})
