#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import newforms as forms
from oi.forum.models import Topic
from oi.st.models import Tag

from oi.st.forms import XssField

#choices = ((u'1', 'Unknown'), (u'2', 'Yes'), (u'3', 'No'))


class TopicForm(forms.Form):
    title = forms.CharField(label='Başlık', required=True, max_length=100, widget=forms.TextInput(attrs={'size': '40',}))
    text = XssField(label='İleti', required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))
    tags=forms.MultipleChoiceField(label='Etiket', required=True,help_text="CTRL basılı tutarak birden fazla etiket seçebilirsiniz!")

    def __init__(self,*args,**kwargs):
        """ It is for topic tihng they are dinamyc"""
        self.base_fields['tags'].choices=[(tag.name,tag.name) for tag in Tag.objects.all()]
        super(TopicForm, self).__init__(*args, **kwargs)

class PostForm(forms.Form):
    text = XssField(label='İleti', required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))

class MergeForm(forms.Form):
    topic2 = forms.ChoiceField(label='Konu', required=True)

    def __init__(self,*args,**kwargs):
        """ It is for topic tihng they are dinamyc"""
        super(MergeForm, self).__init__(*args, **kwargs)
        self.base_fields['topic2'].choices=[(topic.id, topic.title) for topic in Topic.objects.all()]

