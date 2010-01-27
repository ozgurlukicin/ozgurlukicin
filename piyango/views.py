#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.core.mail import EmailMessage
from django.template import Context, loader
from django.shortcuts import get_object_or_404

from oi.forum.views import flood_control
from oi.piyango.forms import PersonForm
from oi.st.wrappers import render_response
from oi.settings import DEFAULT_FROM_EMAIL
from oi.piyango.settings import PIYANGO_MAIL_LIST

def create_person(request):
    if request.method == "POST":
        form = PersonForm(request.POST.copy())
        flood, timeout = flood_control(request)
        if form.is_valid() and not flood:
            person = form.save()
            message = loader.get_template("piyango/confirm_email.html").render(Context({"person":person}))
            mail = EmailMessage("Pardus Çekilişi", message, "Özgürlükiçin <%s>" % DEFAULT_FROM_EMAIL, ["%s <%s>" % (person.get_full_name(), person.email)])
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            return render_response(request, "piyango/sent.html", locals())
    else:
        initial = {}
        if request.user.is_authenticated():
            initial["first_name"] = request.user.first_name
            initial["last_name"] = request.user.last_name
            initial["email"] = request.user.email
            initial["city"] = request.user.get_profile().city
        form = PersonForm(initial=initial)
    return render_response(request, "piyango/create_person.html", locals())

def confirm_person(request, id, hash):
    person = get_object_or_404(Person, id=id, hash=hash, confirmed=False)
    if Person.objects.filter(tcidentity=person.tcidentity, confirmed=True).count()>0:
        return HttpResponse("Bu TC kimlik numarası daha önce kullanılmış!")
    person.confirmed = True
    person.save()
    #send mail to lists
    message = loader.get_template("piyango/confirmed_email.html").render(Context({"person":person,"WEB_URL":WEB_URL}))
    mail = EmailMessage(
        "Pardus Çekilişi",
        message,
        "Özgürlükiçin <%s>" % DEFAULT_FROM_EMAIL,
        [PIYANGO_MAIL_LIST],
        headers={"Message-ID":"%s-%s" % (person.id, person.hash)}
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=True)

    return render_response(request, "piyango/confirmed.html", locals())
