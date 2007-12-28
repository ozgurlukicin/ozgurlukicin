#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import newforms as forms
 
vote_choices=(
				(0,u'Berbat'),
				(1,u'Kötü'),
				(2,u'Orta'),
				(3,u'İyi'),
				(4,u'Güzel'),
				(5,u'Süper'),
				)
class VoteForm(forms.Form):
	""" tema vote form validator"""
	vote= forms.ChoiceField(label="Oy",required=True,choices=vote_choices)

