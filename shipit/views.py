#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage

from oi.shipit.forms import *
from oi.shipit.models import *
from oi.st.wrappers import render_response
from oi.settings import DEFAULT_FROM_EMAIL

def create_cdclient(request):
    if request.method == "POST":
        form = CdClientForm(request.POST.copy())
        if form.is_valid():
            cdClient = form.save()
            message = loader.get_template("templates/shipit/confirm_email.html").render(Context({"cdClient":cdClient}))
            mail = EmailMessage("Pardus CD isteğiniz", message, "Özgürlükiçin <%s>" % DEFAULT_FROM_EMAIL, ["%s <%s>" % (cdClient.get_full_name(), cdClient.email)])
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            return render_response(request, "shipit/sent.html", locals())
    else:
        form = CdClientForm()
    return render_response(request, "shipit/create_cdclient.html", locals())

def confirm_cdclient(self, id, key):
    cdClient = get_object_or_404(CdClient, id=id, hash=hash, confirmed=False)
    cdClient.confirmed = True
    cdClient.save()
    return render_response(request, "shipit/confirmed.html", locals())
