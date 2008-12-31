#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import forms
from django.contrib.auth.models import User

from oi.bug.models import Bug, Comment

class BugForm(forms.ModelForm):
    """
    Bug form. Composed by some Bug model fields.
    """

    class Meta:
        model = Bug
        exclude = ("assigned_to", "submitter", "submitted_date", "status")

class FullBugForm(forms.ModelForm):
    """
    Full bug form. Composed by some Bug model fields.
    """

    def __init__(self,*args,**kwargs):
        """ This is for collecting staff """
        super(FullBugForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].choices=[(user.id, "%s %s" % (user.first_name, user.last_name)) for user in User.objects.filter(is_staff=True).order_by("first_name")]

    class Meta:
        model = Bug
        exclude = ("submitter", "submitted_date")

class CommentForm(forms.ModelForm):
    """
    Comment form. Composed by some Comment model fields.
    """

    class Meta:
        model = Comment
        exclude = ("bug", "author", "date")
