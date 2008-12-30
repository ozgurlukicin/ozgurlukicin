#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404

from oi.seminar.models import Place, Attender, Seminar
from oi.st.wrappers import render_response

def place(request, slug):
    return render_response(request, 'seminar/place.html', locals())
