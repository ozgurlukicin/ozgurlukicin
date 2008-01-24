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
        if self.required and not value:
            raise forms.ValidationError(_(u'Bos birakilamaz'))
        
        #cok strict mi oldu ne  sonra olmazsa uzerinde calisilir :)
        xss_prevent=re.compile('[^A-Za-z0-9, ]')
        
        if re.search(xss_prevent,value):
            raise forms.ValidationError(_(u'Xss mi lutfen ama !'))
            
        return value

class CommentForm(forms.Form):
    """ The comment thngyy add validation please..."""
    yorum=XssField(label="Yorum",required=True,max_length=100,widget=forms.Textarea())

    
