#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Uğur Çetin
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import sha, datetime, random

from django.core.mail import send_mail

from oi.petition.models import PetitionForm, Petitioner
from oi.flatpages.models import FlatPage
from oi.st.wrappers import render_response
from oi.settings import DEFAULT_FROM_EMAIL

def petition_sign(request):
    numberofpetitioners = Petitioner.objects.filter(is_active=True).count()
    petitionpercent = numberofpetitioners / 30

    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            now = datetime.datetime.now()

            petitioner = Petitioner(
                    firstname = form.clean_data['firstname'],
                    lastname = form.clean_data['lastname'],
                    city = form.clean_data['city'],
                    job = form.clean_data['job'],
                    email = form.clean_data['email'],
                    homepage = form.clean_data['homepage'],
                    signed = now,
                    is_active = False,
                    inform = form.clean_data['inform'],
                    )

            # create key taken from profile/views.py
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt).hexdigest()
            petitioner.activation_key = activation_key
            petitioner.save()
            activation_link = "http://www.ozgurlukicin.com/petition/onay/%s/%s" % (petitioner.id, activation_key),

            email_subject = u"Ozgurlukicin.com OOXML'e hayır kampanyası"
            email_body = u"""Merhaba!
OOXML'e karsi yaptigimiz kampanyayi desteklediginiz icin tesekkur ederiz.
Lutfen desteginizi onaylamak icin asagida bulunan adresi ziyaret ederek
onaylama islemini yapiniz.

%s

Tesekkurler,
Ozgurlukicin.com"""

            email_to = form.clean_data['email']

            send_mail(email_subject, email_body % activation_link, DEFAULT_FROM_EMAIL, [email_to], fail_silently=True)

            flatpage = FlatPage.objects.get(url="/ooxml/")
            notconfirmed = True

            return render_response(request, 'petition/sign_done.html', locals())
        else:
            return render_response(request, 'petition/sign.html', locals())
    else:
        petitioners = Petitioner.objects.order_by("-signed").filter(is_active=True)[:20]
        form = PetitionForm()
        flatpage = FlatPage.objects.get(url="/ooxml/")

        return render_response(request, 'petition/sign.html', locals())

def petitioner_confirm(request, pid, key):
    numberofpetitioners = Petitioner.objects.filter(is_active=True).count()
    petitionpercent = numberofpetitioners / 30
    petitioner = Petitioner.objects.get(id=pid)
    if petitioner.is_active:
        already_active = True

        return render_response(request, 'petition/sign_done.html', locals())
    elif petitioner.activation_key == key:
        petitioner.is_active = True
        petitioner.signed = datetime.datetime.now()
        petitioner.save()
        activation_done = True

        return render_response(request, 'petition/sign_done.html', locals())
    else:
        wrongkey = True

        return render_response(request, 'petition/sign_done.html', locals())
