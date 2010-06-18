#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from oi.ideas.models import Idea, RelatedCategory, Status, Related
from oi.st.forms import XssField
from django.utils.translation import ugettext as _

class CommentForm(forms.Form):
    text = forms.CharField(label=_("Your comment"), required=True, widget=forms.Textarea(attrs={ 'cols':'83%', 'rows':'7'}))

class NewIdeaForm(forms.ModelForm):
    title = forms.CharField(label=_("Idea title"), widget=forms.TextInput(attrs={'style':'width: 400px;'}))
    related_to = forms.ModelChoiceField(label=_("Related package"), queryset=Related.objects.order_by("name"), required=False, help_text=_("Can be left blank."))
    class Meta:
        model = Idea
        exclude = ('file',"submitter", "status", "vote_count", "duplicate", "is_hidden", "is_duplicate", "comment_count", "topic")

    def clean_tags(self):
        field_data = self.cleaned_data['tags']
        if len(field_data) > 5:
            raise forms.ValidationError(_("You can choose 5 tags at most. Please choose only relevant tags with your topic."))
        return field_data

#    def __init__(self,*args,**kwargs):
#        super(NewIdeaForm, self).__init__(*args, **kwargs)
#        related_categories = RelatedCategory.objects.all()
#        self.fields['related_to'].choices=[for cat ]
