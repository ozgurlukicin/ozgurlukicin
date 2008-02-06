from django import newforms as forms
import re

class SearchForm(forms.Form):
    term = forms.CharField(label='Anahtar kelime', required=True, widget=forms.TextInput(attrs={'size': '40',}))


class XssField(forms.CharField):
    """ That one will validate the screen upload things"""

    def __init__(self,*args,**kwargs):
        """ Calling the upper function"""
        super(XssField,self).__init__(*args,**kwargs)

    def clean(self,value):
        #for filtering malicious code
        from oi.forum.stripogram import html2text,html2safehtml 

        if self.required and not value:
            raise forms.ValidationError(_(u'Bos birakilamaz'))

        #strip the tags we dont want
        value=html2safehtml(value,valid_tags=('a','b','i','li','img','ul', 'h1', 'h2', 'h3', 'h4', 'h5'))

        if not value:
            raise forms.ValidationError(_(u'Xss mi lutfen ama !'))

        return value

class CommentForm(forms.Form):
    """ The comment thngyy add validation please..."""
    yorum=XssField(label="Yorum",required=True,max_length=100,widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))
