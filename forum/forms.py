#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import date

from django import forms
from oi.forum.models import AbuseReport, Topic, Forum, WatchList
from oi.st.tags import Tag
from oi.poll.models import Poll

from oi.st.forms import XssField
from django.utils.translation import ugettext as _

#choices = ((u'1', 'Unknown'), (u'2', 'Yes'), (u'3', 'No'))


class TopicForm(forms.Form):
    title = forms.CharField(label=_('Title'), required=True, max_length=100, widget=forms.TextInput(attrs={'size': '40',}))
    text = XssField(label=_('Text'), required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))
    tags = forms.MultipleChoiceField(label=_('Tags'), required=True,help_text="CTRL basılı tutarak birden fazla etiket seçebilirsiniz!(En çok 5)")

    def __init__(self,*args,**kwargs):
        """ It is for topic thing they are dynamic"""
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['tags'].choices=[(tag.name, tag.name) for tag in Tag.objects.all()]

    def clean_tags(self):
        field_data = self.cleaned_data['tags']

        # we don't want users to choose more than 5 tags
        if len(field_data) > 5:
            raise forms.ValidationError(_("You can choose 5 tags at most. Please choose only relevant tags with your topic."))

        return field_data

class PostForm(forms.Form):
    text = XssField(label=_('Text'), required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))

class MergeForm(forms.Form):
    topic2 = forms.ChoiceField(label=_('Topic'), required=True)

    def __init__(self,*args,**kwargs):
        """ This is for collecting topics """
        super(MergeForm, self).__init__(*args, **kwargs)
        self.fields['topic2'].choices=[(topic.id, "%s>%s" % (topic.forum, topic.title)) for topic in Topic.objects.order_by("forum")]

class MoveForm(forms.Form):
    forum2 = forms.ChoiceField(label=_("Forum"), required=True)

    def __init__(self,*args,**kwargs):
        """ This is for collecting forums """
        super(MoveForm, self).__init__(*args, **kwargs)
        self.fields['forum2'].choices=[(forum.id, forum.name) for forum in Forum.objects.order_by("name")]

class AbuseForm(forms.Form):
    reason = XssField(label=_('Abuse Reason'), widget=forms.Textarea(attrs={'rows': 7, 'cols': 45}), required=True, help_text=_("(can be 512 characters at most)"), max_length=512)

class PollForm(forms.ModelForm):
    end_date = forms.DateField(label=_("End Date"), required=False, input_formats=("%d/%m/%Y",), help_text=_("Specify when voting will end. like 30/8/2008."))
    option0 = forms.CharField(label=_('1st Choice'), required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option1 = forms.CharField(label=_('2nd Choice'), required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option2 = forms.CharField(label=_('3rd Choice'), required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option3 = forms.CharField(label=_('4th Choice'), required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option4 = forms.CharField(label=_('5th Choice'), required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option5 = forms.CharField(label=_('6th Choice'), required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option6 = forms.CharField(label=_('7th Choice'), required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))
    option7 = forms.CharField(label=_('8th Choice'), required=False, max_length=128, widget=forms.TextInput(attrs={'size': '40',}))

    class Meta:
        model = Poll
        exclude = ("created")

    def clean_end_date(self):
        field_data = self.cleaned_data['end_date']

        # it must be filled if date_limit is on
        if self.cleaned_data["date_limit"] and field_data == None:
            raise forms.ValidationError(_("You have to specify an end date for voting."))

        return field_data
