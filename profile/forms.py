#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re, random, datetime, sha

from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from oi.middleware import threadlocals
from oi.settings import CITY_LIST
from oi.st.models import Contribute
from oi.st.forms import XssField
from oi.profile.models import ForbiddenUsername, Avatar, LostPassword, Profile

class RegisterForm(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı', max_length=20, help_text='En az 3, en fazla 20 karakter')
    firstname = forms.CharField(label='Adı', max_length=30)
    lastname = forms.CharField(label='Soyadı', max_length=30)
    birthday = forms.DateField(label='Doğum Tarihi', input_formats=('%d/%m/%Y', '%d/%m/%Y'), help_text='23/4/1985 gibi')
    email = forms.EmailField(label='E-Posta')
    password = forms.CharField(label='Parola', max_length=32, widget=forms.PasswordInput,)
    password_again = forms.CharField(label='Parola (tekrar)', max_length=32, widget=forms.PasswordInput, help_text='En az 5 karakter')
    city = forms.ChoiceField(label='Şehir', choices=CITY_LIST)
    homepage = forms.URLField(label='Web Sayfası', verify_exists=False, required=False, help_text='(zorunlu değil)')
    msn = forms.EmailField(label='MSN', max_length=50, required=False, help_text='(zorunlu değil)')
    jabber = forms.EmailField(label='Jabber', max_length=50, required=False, help_text='(zorunlu değil)')
    icq = forms.CharField(label='ICQ', max_length=15, required=False, help_text='(zorunlu değil)')
    contributes = forms.ModelMultipleChoiceField(label='Katkı Başlıkları', queryset=Contribute.objects.all(), required=False, help_text='Bize nasıl katkıda bulunabilirsiniz? (ctrl ile birden fazla seçim yapılabilir, zorunlu değil)')
    contributes_summary = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'rows': 7, 'cols': 45}), required=False, help_text='Katkı sağlayabilecekseniz açıklama yazın (zorunlu değil)')
    show_email = forms.BooleanField(label='E-posta Adresini Göster', required=False, help_text='Profil sayfasında diğerleri e-posta adresinizi görebilsin mi?')
    show_birthday = forms.BooleanField(label='Doğum Tarihini Göster', required=False, help_text='Profil sayfasında diğerleri doğum tarihinizi görebilsin mi?')

    def clean_username(self):
        field_data = self.cleaned_data['username']

        if len(field_data) < 3:
            raise forms.ValidationError(u"Kullanıcı adı en az 3 karakter olmalıdır")

        if not re.match("[a-zA-Z0-9_]+$", field_data):
            raise forms.ValidationError(u"Kullanıcı adı geçersiz. Kullanıcı adı sadece \"a-z A-Z 0-9 _\" karakterlerinden oluşabilir")

        forbidden = ForbiddenUsername.objects.filter(name__iexact=field_data)
        if len(forbidden) > 0:
            raise forms.ValidationError(u"Bu kullanıcı adının alınması yasaklanmış")

        u = User.objects.filter(username__iexact=field_data)
        if len(u) > 0:
            raise forms.ValidationError(u"Bu kullanıcı adı daha önce alınmış")

        return field_data

    def clean_email(self):
        field_data = self.cleaned_data['email']

        if not field_data:
            return ''

        u = User.objects.filter(email=field_data)
        if len(u) > 0:
            raise forms.ValidationError(u"Bu e-posta adresi ile daha önceden kayıt yapılmış")

        return field_data

    def clean_password_again(self):
        field_data = self.cleaned_data['password_again']

        if not self.cleaned_data.has_key('password'):
            return
        else:
            password = self.cleaned_data['password']

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

        if len(field_data) < 5:
            raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

        if (password or field_data) and password != field_data:
                    raise forms.ValidationError(u"Parolalar eşleşmiyor")

        return field_data

    def clean_icq(self):
        field_data = self.cleaned_data['icq']
        if field_data == "":
            return field_data
        try:
            number = int(field_data)
            if number < 0:
                raise forms.ValidationError(u"ICQ numarası pozitif bir tamsayı olmalıdır")
            return field_data
        except ValueError:
            raise forms.ValidationError(u"ICQ numarası sayılardan oluşmalıdır")

class ProfileEditForm(forms.Form):
    avatar = forms.ChoiceField(label='Avatar', widget=forms.Select(attrs={"onchange":"updateAvatar(this)", "onkeyup":"updateAvatar(this)"}))
    firstname = forms.CharField(label='Adı', max_length=30)
    lastname = forms.CharField(label='Soyadı', max_length=30)
    birthday = forms.DateField(label='Doğum Tarihi', input_formats=('%d/%m/%Y', '%d/%m/%y'), help_text='23/4/1985 gibi')
    email = forms.EmailField(label='E-posta')
    city = forms.ChoiceField(label='Şehir', choices=CITY_LIST)
    homepage = forms.URLField(label='Ana Sayfa', required=False, help_text='http:// ile başlamayı unutmayın')
    msn = forms.EmailField(label='MSN', max_length=50, required=False)
    jabber = forms.EmailField(label='Jabber', max_length=50, required=False)
    icq = forms.CharField(label='ICQ', max_length=15, required=False)
    show_email = forms.BooleanField(label='E-posta Adresini Göster', required=False, help_text='Profil sayfasında diğerleri e-posta adresinizi görsün mü?')
    show_birthday = forms.BooleanField(label='Doğum Tarihini Göster', required=False, help_text='Profil sayfasında diğerleri doğum tarihinizi görebilsin mi?')
    bio = XssField(label="Kendinizi Tanıtın", required=False, help_text="Burada kısaca kendinizi tanıtabilirsiniz. Yazdıklarınız profilinizde görünecektir.", max_length=2048, widget=forms.Textarea(attrs={'rows': 7, 'cols': 45}))
    signature = XssField(label='İmza', widget=forms.Textarea(attrs={'rows': 7, 'cols': 45}), required=False, help_text='Forumdaki her iletinizin altında görünecek imzanız (html tagları kullanabilirsiniz, en fazla 512 karakter olabilir)', max_length=512)
    latitude = forms.DecimalField(label='Enlem', max_digits=10, decimal_places=6)
    longitude = forms.DecimalField(label='Boylam', max_digits=10, decimal_places=6)

    def __init__(self,*args,**kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].choices = [(avatar.file, avatar.name) for avatar in Avatar.objects.order_by("name")]

    def set_user(self, user):
        self.user = user

    def clean_icq(self):
        field_data = self.cleaned_data['icq']
        if field_data == "":
            return field_data
        try:
            number = int(field_data)
            if number < 0:
                raise forms.ValidationError(u"ICQ numarası pozitif bir tamsayı olmalıdır")
            return field_data
        except ValueError:
            raise forms.ValidationError(u"ICQ numarası sayılardan oluşmalıdır")

    def clean_email(self):
        field_data = self.cleaned_data['email']

        if not field_data:
            return ''

        try:
            u = User.objects.get(email=field_data)
            if not u.id == self.user.id:
                raise forms.ValidationError(u"Bu e-posta adresi ile başka birisi daha önceden kayıt yapmış")
        except ObjectDoesNotExist:
            pass

        return field_data

class LostPasswordForm(forms.Form):
    username = forms.CharField(label='Kullanıcı adı', max_length=30)
    email = forms.EmailField(label='E-posta')

    def clean_username(self):
        # clean old keys when it's requested
        old_keys = LostPassword.objects.filter(key_expires__lt=datetime.date.today())
        for key in old_keys: key.delete()

        field_data = self.cleaned_data['username']

        # control username whether it exists or not
        if len(User.objects.filter(username__iexact=field_data)) == 0:
            raise forms.ValidationError(u"Böyle bir kullanıcı yok")

        # control if this user has requested a new password
        if len(LostPassword.objects.filter(user__username__iexact=field_data)) > 0:
            raise forms.ValidationError(u"Bu kullanıcı daha önce parola isteğinde bulunmuş")

        return field_data

    def clean_email(self):
        field_data = self.cleaned_data['email']

        if not self.cleaned_data.has_key('username'):
            return
        else:
            username = self.cleaned_data['username']

        # control email if it is correct
        try:
            u = User.objects.get(username=username)
            if u.email != field_data:
                raise forms.ValidationError(u"E-mail adresi uyuşmuyor")
        except User.DoesNotExist:
            pass

        return field_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Eski Parola', widget=forms.PasswordInput, required=False)
    password = forms.CharField(label='Parola', widget=forms.PasswordInput, required=False, help_text='Değiştirmek istiyorsanız her ikisini de doldurun')
    password_again = forms.CharField(label='Parola (Tekrar)', widget=forms.PasswordInput, required=False)

    def set_user(self, user):
        self.user = user

    def clean_old_password(self):
        field_data = self.cleaned_data['old_password']

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

        if len(field_data) > 32:
            raise forms.ValidationError(u"Parola en fazla 32 karakter olmalıdır")

        if len(field_data) < 5:
            raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

        return field_data

    def clean_password(self):
        field_data = self.cleaned_data['password']

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

        if len(field_data) > 32:
            raise forms.ValidationError(u"Parola en fazla 32 karakter olmalıdır")

        if len(field_data) < 5:
            raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

        return field_data

    def clean_password_again(self):
        field_data = self.cleaned_data['password_again']

        if not self.cleaned_data.has_key('password') or not self.cleaned_data.has_key('old_password'):
            return
        else:
            password = self.cleaned_data['password']
            old_password = self.cleaned_data['old_password']

        if old_password or password or field_data:
            if field_data and password and old_password:
                if len(field_data.split(' ')) != 1:
                    raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

                if len(field_data) > 32:
                    raise forms.ValidationError(u"Parola en fazla 32 karakter olmalıdır")

                if len(field_data) < 5:
                    raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

                if (password or field_data) and password != field_data:
                    raise forms.ValidationError(u"Parolalar eşleşmiyor")

                u = User.objects.get(username=self.user.username)
                if not u.check_password(old_password):
                    raise forms.ValidationError(u"Eski parola yanlış")

                return field_data
            else:
                raise forms.ValidationError(u"Parolayı değiştirmek için her 3 alanı da doldurun")
        else:
            return ''

class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='Parola', widget=forms.PasswordInput, max_length=32, min_length=5)
    password_again = forms.CharField(label='Parola (Tekrar)', widget=forms.PasswordInput, max_length=32, min_length=5)

    def clean_password_again(self):
        field_data = self.cleaned_data['password_again']

        if not self.cleaned_data.has_key('password'):
            return
        else:
            password = self.cleaned_data['password']

        if field_data != password:
            raise forms.ValidationError('Parolalar eşleşmiyor')

        return field_data
