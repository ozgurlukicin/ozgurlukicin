#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404

from oi.seminar.models import Place, Attender, Seminar
from oi.st.wrappers import render_response

def attender(request, slug):
    return render_response(request, 'seminar/attender.html', locals())

def place(request, slug):
    return render_response(request, 'seminar/place.html', locals())

"""
@permission_required('seminar.change_seminar', login_url="/kullanici/giris/")
def send_notification(request):
    if request.method == "POST":
        city = form.cleaned_data["city"]
        users = Profile.objects.filter(user__is_active=True, city=city)
        subject = "Özgürlükİçin Seminer Bildirisi"
        message = "Sayın %(fullname)s, %(date)s tarihinde %(place)s adresinde %(title)s konulu bir seminer verilecektir. Bu e-postayı %(city)s şehrinde bulunduğunuzu belirttiğiniz için alıyorsunuz. Bir daha özgürlükiçin seminerleri için bildiri almak istemiyorsanız bu adresi ziyaret edin: %(dontspammelink)s"
        mails = []
        mail_dict = {
            "date": seminar.date,
            "place": seminar.place,
            "title": seminar.date,
        }
        for user in users:
            mail_dict["fullname"] = user.user.get_full_name()
            mails.append(subject, message % mail_dict, DEFAULT_FROM_EMAIL, (user.user.email,))
        send_mass_mail(mails, fail_silently=True)
"""
