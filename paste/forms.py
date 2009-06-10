#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import forms
from oi.paste.models import PastedText

class PastedTextForm(forms.ModelForm):
    class Meta:
        model = PastedText
        exclude = ("author", "ip", "is_hidden", "highlighted_text")
