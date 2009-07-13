#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.contrib.auth.decorators import permission_required
from django.views.generic.list_detail import object_list

from oi.shipit.forms import *
from oi.shipit.models import *
from oi.shipit.settings import *
from oi.st.wrappers import render_response
from oi.settings import DEFAULT_FROM_EMAIL
from oi.forum.views import flood_control

def create_cdclient(request):
    if request.method == "POST":
        form = CdClientForm(request.POST.copy())
        flood, timeout = flood_control(request)
        if form.is_valid() and not flood:
            cdClient = form.save()
            message = loader.get_template("shipit/confirm_email.html").render(Context({"cdClient":cdClient}))
            mail = EmailMessage("Pardus CD isteğiniz", message, "Özgürlükiçin <%s>" % DEFAULT_FROM_EMAIL, ["%s <%s>" % (cdClient.get_full_name(), cdClient.email)])
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            return render_response(request, "shipit/sent.html", locals())
    else:
        initial = {}
        if request.user.is_authenticated():
            initial["first_name"] = request.user.first_name
            initial["last_name"] = request.user.last_name
            initial["email"] = request.user.email
            initial["city"] = request.user.get_profile().city
        form = CdClientForm(initial=initial)
    return render_response(request, "shipit/create_cdclient.html", locals())

def confirm_cdclient(request, id, hash):
    cdClient = get_object_or_404(CdClient, id=id, hash=hash, confirmed=False)
    cdClient.confirmed = True
    cdClient.save()
    #send mail to lists
    message = loader.get_template("shipit/confirmed_email.html").render(Context({"cdClient":cdClient}))
    mail = EmailMessage(
        "Pardus CD isteği",
        message,
        "Özgürlükiçin <%s>" % DEFAULT_FROM_EMAIL,
        [CD_MAIL_LIST],
        headers={"Message-ID":"%s-%s" % (cdClient.id, cdClient.hash)}
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=True)

    return render_response(request, "shipit/confirmed.html", locals())

@permission_required("shipit.change_cdclient")
def cdclient_list(request):
    cdClients = CdClient.objects.filter(confirmed=True)
    return object_list(
        request,
        cdClients,
        paginate_by = CDCLIENTS_PER_PAGE,
        allow_empty = True,
    )

@permission_required("shipit.change_cdclient")
def change_cdclient(request, id):
    cdClient = get_object_or_404(CdClient, id=id)
    if request.method == "POST":
        form = CdClientChangeForm(request.POST, instance=cdClient)
        if form.is_valid():
            form.save()
    else:
        form = CdClientChangeForm(instance=cdClient)
    return render_response(request, "shipit/change_cdclient.html", locals())

@permission_required("shipit.change_cdclient")
def cdclient_detail(request, id):
    cdClient = get_object_or_404(CdClient, id=id)
    return render_response(request, "shipit/cdclient_detail.html", locals())
