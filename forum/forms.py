#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import date

from django import newforms as forms
from oi.forum.models import AbuseReport, Topic, Forum, WatchList
from oi.st.models import Tag
from oi.poll.models import Poll

from oi.st.forms import XssField

#choices = ((u'1', 'Unknown'), (u'2', 'Yes'), (u'3', 'No'))


class TopicForm(forms.Form):
    title = forms.CharField(label='Başlık', required=True, max_length=100, widget=forms.TextInput(attrs={'size': '40',}))
    text = XssField(label='İleti', required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))
    tags = forms.MultipleChoiceField(label='Etiket', required=True,help_text="CTRL basılı tutarak birden fazla etiket seçebilirsiniz!(En çok 5)")

    def __init__(self,*args,**kwargs):
        """ It is for topic thing they are dynamic"""
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['tags'].choices=[(tag.name, tag.name) for tag in Tag.objects.all()]

    def clean_tags(self):
        field_data = self.cleaned_data['tags']

        # we don't want users to choose more than 5 tags
        if len(field_data) > 5:
            raise forms.ValidationError("En fazla 5 etiket seçebilirsiniz. Lütfen açtığınız başlığa uygun etiket seçiniz.")

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

class AbuseForm(forms.Form):
    reason = XssField(label='Şikayet Sebebi', widget=forms.Textarea(attrs={'rows': 7, 'cols': 45}), required=True, help_text="(en fazla 512 karakter olabilir)", max_length=512)

class PollForm(forms.ModelForm):
    end_date = forms.DateField(label="Bitiş Tarihi", required=False, input_formats=("%d/%m/%Y",), help_text="Oylamanın ne zaman biteceğini belirleyin. 30/8/2008 gibi.")
    option0 = forms.CharField(label='1. Seçenek', required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option1 = forms.CharField(label='2. Seçenek', required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option2 = forms.CharField(label='3. Seçenek', required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option3 = forms.CharField(label='4. Seçenek', required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option4 = forms.CharField(label='5. Seçenek', required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option5 = forms.CharField(label='6. Seçenek', required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option6 = forms.CharField(label='7. Seçenek', required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option7 = forms.CharField(label='8. Seçenek', required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))

    class Meta:
        model = Poll
        exclude = ("created")

    def clean_end_date(self):
        field_data = self.cleaned_data['end_date']

        # it must be filled if date_limit is on
        if self.cleaned_data["date_limit"] and field_data == None:
            raise forms.ValidationError("Oylama bitiş tarihini belirlemelisiniz.")

        return field_data
