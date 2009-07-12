#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from oi.shipit.forms import *
from oi.shipit.models import *
from oi.st.wrappers import render_response

def create_cdclient(request):
    if request.method == "POST":
        form = CdClientForm(request.POST.copy())
        if form.is_valid():
            cdClient = form.save()
            #TODO: send mails
    else:
        form = CdClientForm()
    return render_response(request, "shipit/create_cdclient.html", locals())
