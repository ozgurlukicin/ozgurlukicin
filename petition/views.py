#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Uğur Çetin
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime

from oi.petition.models import PetitionForm, Petitioner
from oi.flatpages.models import FlatPage
from oi.st.wrappers import render_response

def petition_sign(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petitioner = Petitioner(
                    firstname = form.clean_data['firstname'],
                    lastname = form.clean_data['lastname'],
                    city = form.clean_data['city'],
                    job = form.clean_data['job'],
                    email = form.clean_data['email'],
                    homepage = form.clean_data['homepage'],
                    signed = datetime.now(),
                    )
            petitioner.save()
            flatpage = FlatPage.objects.get(url="/ooxml/")

            return render_response(request, 'petition/sign_done.html', locals())
        else:
            return render_response(request, 'petition/sign.html', locals())
    else:
        petitioners = Petitioner.objects.order_by("-signed")[:20]
        numberofpetitioners = Petitioner.objects.count()
        petitionpercent = numberofpetitioners / 30
        form = PetitionForm()
        flatpage = FlatPage.objects.get(url="/ooxml/")
        return render_response(request, 'petition/sign.html', locals())
