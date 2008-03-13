from django import newforms as forms
import re

class SearchForm(forms.Form):
    term = forms.CharField(label='Anahtar kelime', required=True, widget=forms.TextInput(attrs={'size': '40',}))

class XssField(forms.CharField):
    """ That one will validate the screen upload things"""

    def __init__(self,*args,**kwargs):
        """ Calling the upper function"""
        super(XssField,self).__init__(*args,**kwargs)

class CommentForm(forms.Form):
    """ The comment thingy add validation please..."""
    yorum=XssField(label="Yorum",required=True,max_length=1000,widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))
