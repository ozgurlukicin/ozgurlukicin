#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Uğur Çetin
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import newforms as forms

from oi.bug.models import Bug

class BugForm(forms.ModelForm):
    """
    Bug form. Composed by all the Bug model fields.
    """

    class Meta:
        model = Bug
        exclude = ("assigned_to", "submitter", "submitted_date", "status")
