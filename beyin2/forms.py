#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import forms
from oi.beyin2.models import Idea

class IdeaForm(forms.ModelForm):
    class Meta:
	model = Idea
	exclude = ('dateSubmitted', 'submitter','topic','is_hidden','duplicate','is_duplicate')
