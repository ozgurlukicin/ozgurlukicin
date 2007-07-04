#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re

from django.db import models
from django.contrib.auth.models import User
from django import newforms as forms

from oi.middleware import threadlocals
from oi.settings import CITY_LIST
from oi.st.models import Contribute

class ForbiddenUsername(models.Model):
    name = models.CharField("Kullanıcı adı", maxlength=30)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name',)
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        verbose_name = "Yasaklanan Kullanıcı Adı"
        verbose_name_plural = "Yasaklanan Kullanıcı Adları"

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    birthday = models.DateField(blank=True)
    homepage = models.URLField('Ana Sayfa', blank=True, verify_exists=False, unique=False)
    im = models.EmailField('IM', maxlength=50, blank=True)
    city = models.CharField('Şehir', blank=True, choices=CITY_LIST, maxlength=40)
    show_email = models.BooleanField('E-posta Göster', default=0)
    contributes = models.ManyToManyField(Contribute, blank=True, verbose_name='Katkılar')
    contributes_summary = models.TextField('Katkı Açıklaması', blank=True)
    activation_key = models.CharField(maxlength=40)
    key_expires = models.DateTimeField()

    def __str__(self):
        return self.user.username

    class Admin:
        fields = (
            ('Üyelik Bilgileri', {'fields': ('user', 'homepage','im', 'city', 'birthday', 'contributes', 'contributes_summary', 'show_email',)}),
            ('Diğer', {'fields': ('activation_key', 'key_expires'), 'classes': 'collapse',}),
        )

        list_display = ('user', 'city',)
        ordering = ['-user']
        search_fields = ['user']

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"

class RegisterForm(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı', max_length=30, help_text='En az 3, en fazla 30 karakter')
    firstname = forms.CharField(label='İsim', max_length=30)
    lastname = forms.CharField(label='Soyisim', max_length=30)
    birthday = forms.DateField(label='Doğum Tarihi', help_text='10/5/1985 gibi.')
    email = forms.EmailField(label='E-Posta')
    password = forms.CharField(label='Parola', max_length=32, widget=forms.PasswordInput,)
    password_again = forms.CharField(label='Parola (tekrar)', max_length=32, widget=forms.PasswordInput, help_text='En az 5 karakter')
    city = forms.ChoiceField(label='Şehir', choices=CITY_LIST)
    homepage = forms.URLField(label='Web Sayfası', verify_exists=False, required=False, help_text='(zorunlu değil)')
    contributes = forms.ModelMultipleChoiceField(label='Katkı Başlıkları', queryset=Contribute.objects.all(), required=False, help_text='Bize nasıl katkıda bulunabilirsiniz? (ctrl ile birden fazla seçim yapılabilir, zorunlu değil)')
    contributes_summary = forms.CharField(label='Açıklama', widget=forms.Textarea, required=False, help_text='Katkı sağlayabilecekseniz açıklama yazın (zorunlu değil)')
    show_email = forms.BooleanField(label='E-posta Adresini Göster', required=False, help_text='Profil sayfasında diğerleri e-posta adresinizi görebilsin mi?')

    def clean_username(self):
        field_data = self.clean_data['username']

        if not field_data:
            return ''

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(u"Kullanıcı adında boşluk olmamalıdır")

        if len(field_data) < 3:
            raise forms.ValidationError(u"Kullanıcı adı en az 3 karakter olmalıdır")

        regexp = re.compile("\w+")
        if not regexp.match(field_data):
            raise forms.ValidationError(u"Kullanıcı adı geçersiz")

        forbidden = ForbiddenUsername.objects.filter(name__iexact=field_data)
        if len(forbidden) > 0:
            raise forms.ValidationError(u"Bu kullanıcı adının alınması yasaklanmış")

        u = User.objects.filter(username__iexact=field_data)
        if len(u) > 0:
            raise forms.ValidationError(u"Bu kullanıcı adı daha önce alınmış")

        return self.clean_data['username']


    def clean_password_again(self):
        field_data = self.clean_data['password_again']
        password = self.clean_data['password']
        if not field_data:
            return ''

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

        if len(field_data) < 5:
            raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

        if (password or field_data) and password != field_data:
                    raise forms.ValidationError(u"Parolalar eşleşmiyor")

        return field_data

class ProfileEditForm(forms.Form):
    firstname = forms.CharField(label='İsim', max_length=30)
    lastname = forms.CharField(label='Soyisim', max_length=30)
    birthday = forms.DateField(label='Doğum Tarihi', help_text='10/5/1985 gibi.')
    email = forms.EmailField(label='E-posta')
    city = forms.ChoiceField(label='Şehir', choices=CITY_LIST)
    homepage = forms.URLField(label='Ana Sayfa', required=False, help_text='http:// ile başlamayı unutmayın')
    old_password = forms.CharField(label='Eski Parola', widget=forms.PasswordInput, max_length=32, required=False)
    password = forms.CharField(label='Parola', widget=forms.PasswordInput, max_length=32, required=False, help_text='Değiştirmek istiyorsanız her ikisini de doldurun')
    password_again = forms.CharField(label='Parola (yeniden)', widget=forms.PasswordInput, max_length=32, required=False)
    show_email = forms.BooleanField(label='E-posta Adresini Göster', required=False, help_text='Profil sayfasında diğerleri e-posta adresinizi görsün mü?')

    def set_user(self, user):
        self.user = user

    def clean_old_password(self):
        field_data = self.clean_data['old_password']
        if not field_data:
            return ''
        else:
            if len(field_data.split(' ')) != 1:
                raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

            if len(field_data) < 5:
                raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

            return field_data

    def clean_password(self):
        field_data = self.clean_data['password']
        if not field_data:
            return ''
        else:
            if len(field_data.split(' ')) != 1:
                raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

            if len(field_data) < 5:
                raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

            return field_data

    def clean_password_again(self):
        field_data = self.clean_data['password_again']
        password = self.clean_data['password']
        old_password = self.clean_data['old_password']

        if old_password or password or field_data:
            if field_data and password and old_password:
                if len(field_data.split(' ')) != 1:
                    raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

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
