#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import forms

from oi.tema.models import ThemeItem

vote_choices=(
    (0,   '1'),
    (25,  '2'),
    (50,  '3'),
    (75,  '4'),
    (100, '5'),
)

class ThemeItemForm(forms.ModelForm):
    class Meta:
        model = ThemeItem
        exclude = ("parentcategory", "author", "rating", "download_count", "submit_date", "edit_date", "approved")
