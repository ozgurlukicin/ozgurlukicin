#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import newforms as forms
from oi.forum.models import Topic, Forum
from oi.st.models import Tag

from oi.st.forms import XssField

#choices = ((u'1', 'Unknown'), (u'2', 'Yes'), (u'3', 'No'))


class TopicForm(forms.Form):
    title = forms.CharField(label='Başlık', required=True, max_length=100, widget=forms.TextInput(attrs={'size': '40',}))
    text = XssField(label='İleti', required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))
    tags = forms.MultipleChoiceField(label='Etiket', required=True,help_text="CTRL basılı tutarak birden fazla etiket seçebilirsiniz!(En çok 5)")

    def __init__(self,*args,**kwargs):
        """ It is for topic tihng they are dinamyc"""
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['tags'].choices=[(tag.name, tag.name) for tag in Tag.objects.all()]

    def clean_tags(self):
        field_data = self.cleaned_data['tags']

        # we don't want users to choose more than 5 tags
        if len(field_data) > 5:
            raise forms.ValidationError("En fazla 5 tag seçebilirsiniz. Lütfen açtığınız başlığa uygun tag seçin")

        return field_data

class PostForm(forms.Form):
    text = XssField(label='İleti', required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))

class MergeForm(forms.Form):
    topic2 = forms.ChoiceField(label='Konu', required=True)

    def __init__(self,*args,**kwargs):
        """ This is for collecting topics """
        super(MergeForm, self).__init__(*args, **kwargs)
        self.fields['topic2'].choices=[(topic.id, "%s>%s" % (topic.forum, topic.title)) for topic in Topic.objects.order_by("forum")]

class MoveForm(forms.Form):
    forum2 = forms.ChoiceField(label="Forum", required=True)

    def __init__(self,*args,**kwargs):
        """ This is for collecting forums """
        super(MoveForm, self).__init__(*args, **kwargs)
        self.fields['forum2'].choices=[(forum.id, forum.name) for forum in Forum.objects.order_by("name")]
