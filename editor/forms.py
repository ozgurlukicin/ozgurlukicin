#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import forms
from oi.st.models import News

class ContributesNewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ("update", "status", "topic")
