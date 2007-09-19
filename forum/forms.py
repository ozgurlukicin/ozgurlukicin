from django import newforms as forms

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class TopicForm(forms.Form):
    title = forms.CharField(label='Başlık', required=True, max_length=100, widget=forms.TextInput(attrs={'size': '40',}))
    text = forms.CharField(label='İleti', required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))

class PostForm(forms.Form):
    text = forms.CharField(label='İleti', required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))