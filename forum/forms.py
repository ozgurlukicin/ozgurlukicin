from django import newforms as forms

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class TopicForm(forms.Form):
    title = forms.CharField(label='Başlık', required=True, max_length=100, widget=forms.TextInput(attrs={'size': '40',}))
    text = forms.CharField(label='İleti', required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))

class PostForm(forms.Form):
    post = forms.CharField(
            label = '',
            widget=forms.Textarea(attrs={'rows':'5', 'cols':'10',}),   )


class ThreadForm(forms.Form):
    subject = forms.CharField(max_length=80,
            widget=forms.TextInput(
                attrs={
                    'size': '80',
                })
            )
    post = forms.CharField(widget=forms.Textarea(
            attrs={
                'rows':'5',
                'cols': '80',
            })
        )

    def clean_category(self):
        id = int(self.cleaned_data['category'])
        return id


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        scd = self.cleaned_data
        self.user = authenticate(username=scd['username'], password=scd['password'])

        if self.user is not None:
            if self.user.is_active:
                return self.cleaned_data['password']
            else:
                raise ValidationError('Your account has been disabled.')
        else:
            raise ValidationError('Your username or password were incorrect.')
# vim: ai ts=4 sts=4 et sw=4
 
