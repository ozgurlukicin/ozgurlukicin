#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Uğur Çetin
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import newforms as forms

from oi.bug.models import Bug, Comment

class BugForm(forms.ModelForm):
    """
    Bug form. Composed by some Bug model fields.
    """

    class Meta:
        model = Bug
        exclude = ("assigned_to", "submitter", "submitted_date", "status")

class CommentForm(forms.ModelForm):
    """
    Comment form. Composed by some Comment model fields.
    """

    class Meta:
        model = Comment
        exclude = ("bug", "author", "date")
