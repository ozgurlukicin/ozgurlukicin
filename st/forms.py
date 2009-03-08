#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007, 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from BeautifulSoup import BeautifulSoup, Comment
from django import forms
import re

class SearchForm(forms.Form):
    term = forms.CharField(label='Anahtar kelime', required=True, widget=forms.TextInput(attrs={'size': '40',}))

class AdvancedSearchForm(forms.Form):
    term = forms.CharField(label='Anahtar kelime', required=True, min_length=3, widget=forms.TextInput(attrs={'size': '40',}))
    search_in = forms.ChoiceField(label="Aranacak Bölümler", widget=forms.RadioSelect, choices=(
        (0, "Forum"),
        (1, "Diğer Bölümler"),
        (2, "Tümü"),
        ))
    depth = forms.ChoiceField(label="Arama Derinliği", widget=forms.RadioSelect, choices=(
        (0, "Sadece Başlıklarda Ara"),
        (1, "Başlıklarda ve İçerikte Ara"),
        ))

class XssField(forms.CharField):
    """ That one will validate the screen upload things"""

    def __init__(self,*args,**kwargs):
        """ Calling the upper function"""
        super(XssField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(XssField, self).clean(value)
        validTags = "address em p i strong b u a h1 h2 h3 h4 h5 h6 pre br img span sub sup ol ul li".split()
        validAttrs = "align alt border href src style target title".split()
        soup = BeautifulSoup(value)
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
        for tag in soup.findAll(True):
            if tag.name not in validTags:
                tag.hidden = True
            elif tag.name == "a":
                tag["target"] = "_blank"
            tag.attrs = [(attr, val) for attr, val in tag.attrs if attr in validAttrs]
        return soup.renderContents().decode('utf8')

class CommentForm(forms.Form):
    """ The comment thingy add validation please..."""
    yorum=XssField(label="Yorum",required=True,max_length=1000,widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))
