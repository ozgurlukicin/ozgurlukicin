#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
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
from django.utils.translation import ugettext as _

class RegisterForm(forms.Form):
    username = forms.CharField(label=_("Username"), max_length=20, help_text=_("Minimum 3, maximum 20 characters"))
    firstname = forms.CharField(label=_("Name"), max_length=30)
    lastname = forms.CharField(label=_("Surname"), max_length=30)
    birthday = forms.DateField(label=_("Birth Date"), input_formats=('%d/%m/%Y', '%d/%m/%Y'), help_text=_("like 23/4/1985"))
    email = forms.EmailField(label=_("E-mail"))
    password = forms.CharField(label=_("Password"), max_length=32, widget=forms.PasswordInput,)
    password_again = forms.CharField(label=_("Password (again)"), max_length=32, widget=forms.PasswordInput, help_text=_("Minimum 5 characters"))
    city = forms.ChoiceField(label=_("City"), choices=CITY_LIST)
    homepage = forms.URLField(label=_("Web Page"), verify_exists=False, required=False, help_text=_("Not required"))
    msn = forms.EmailField(label='MSN', max_length=50, required=False, help_text=_("Not required"))
    jabber = forms.EmailField(label='Jabber', max_length=50, required=False, help_text=_("Not required"))
    icq = forms.CharField(label='ICQ', max_length=15, required=False, help_text=_("Not required"))
    contributes = forms.ModelMultipleChoiceField(label=_("Contributions"), queryset=Contribute.objects.all(), required=False, help_text=_("How can you contribute our community? (you may select more than one choice with holding down ctrl key, not required)"))
    contributes_summary = forms.CharField(label=_("Contribution comment"), widget=forms.Textarea(attrs={'rows': 7, 'cols': 45}), required=False, help_text=_("Make comments about your contribution (not required)"))
    show_email = forms.BooleanField(label=_("Show my e-mail address"), required=False, help_text=_("Do you want other members to see your e-mail address in your profile page?"))
    show_birthday = forms.BooleanField(label=_("Show birth date"), required=False, help_text=_("Do you want other members to see your birth date in your profile page?"))

    def clean_username(self):
        field_data = self.cleaned_data['username']

        if len(field_data) < 3:
            raise forms.ValidationError(_("Username must be at least 3 characters long"))

        if not re.match("[a-zA-Z0-9_]+$", field_data):
            raise forms.ValidationError(_("Invalid username. Username can only contain \"a-z A-Z 0-9 _\" characters"))

        forbidden = ForbiddenUsername.objects.filter(name__iexact=field_data)
        if len(forbidden) > 0:
            raise forms.ValidationError(_("This username is forbidden"))

        u = User.objects.filter(username__iexact=field_data)
        if len(u) > 0:
            raise forms.ValidationError(_("This username is in use"))

        return field_data

    def clean_email(self):
        field_data = self.cleaned_data['email']

        if not field_data:
            return ''

        u = User.objects.filter(email=field_data)
        if len(u) > 0:
            raise forms.ValidationError(_("This e-mail address is in use"))

        return field_data

    def clean_password_again(self):
        field_data = self.cleaned_data['password_again']

        if not self.cleaned_data.has_key('password'):
            return
        else:
            password = self.cleaned_data['password']

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(_("Password may not contain space character"))

        if len(field_data) < 5:
            raise forms.ValidationError(_("Password must be at least 5 characters long"))

        if (password or field_data) and password != field_data:
                    raise forms.ValidationError(_("Passwords don't match"))

        return field_data

    def clean_icq(self):
        field_data = self.cleaned_data['icq']
        if field_data == "":
            return field_data
        try:
            number = int(field_data)
            if number < 0:
                raise forms.ValidationError(_("ICQ number must be a positive integer"))
            return field_data
        except ValueError:
            raise forms.ValidationError(_("ICQ number can only contain numbers"))

class ProfileEditForm(forms.Form):
    avatar = forms.ChoiceField(label=_("Avatar"), widget=forms.Select(attrs={"onchange":"updateAvatar(this)", "onkeyup":"updateAvatar(this)"}))
    firstname = forms.CharField(label=_("Name"), max_length=30)
    lastname = forms.CharField(label=_("Surname"), max_length=30)
    birthday = forms.DateField(label=_("Birth Date"), input_formats=('%d/%m/%Y', '%d/%m/%y'), help_text='23/4/1985 gibi')
    email = forms.EmailField(label=_("E-mail"))
    city = forms.ChoiceField(label=_("City"), choices=CITY_LIST)
    homepage = forms.URLField(label=_("Web Page"), required=False, help_text="Start with http://")
    msn = forms.EmailField(label='MSN', max_length=50, required=False)
    jabber = forms.EmailField(label='Jabber', max_length=50, required=False)
    icq = forms.CharField(label='ICQ', max_length=15, required=False)
    show_email = forms.BooleanField(label=_("Show e-mail address"), required=False, help_text=_("Do you want other members to see your e-mail address in your profile page?"))
    show_birthday = forms.BooleanField(label=_("Show birth date"), required=False, help_text=_("Do you want other members to see your birth date in your profile page?"))
    bio = XssField(label=_("Introduce yourself"), required=False, help_text=_("Here, you can introduce yourself briefly. This will be shown in your profile page."), max_length=2048, widget=forms.Textarea(attrs={'rows': 7, 'cols': 45}))
    signature = XssField(label=_("Signature"), widget=forms.Textarea(attrs={'rows': 7, 'cols': 45}), required=False, help_text=_("This will be shown under your posts in forum pages (512 characters max.)"), max_length=512)
    latitude = forms.DecimalField(label=_("Latitude"), max_digits=10, decimal_places=6)
    longitude = forms.DecimalField(label=_("Longitude"), max_digits=10, decimal_places=6)

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
                raise forms.ValidationError(_("ICQ number must be a positive integer"))
            return field_data
        except ValueError:
            raise forms.ValidationError(_("ICQ number can only contain numbers"))

    def clean_email(self):
        field_data = self.cleaned_data['email']

        if not field_data:
            return ''

        try:
            u = User.objects.get(email=field_data)
            if not u.id == self.user.id:
                raise forms.ValidationError(_("This e-mail address is in use"))
        except ObjectDoesNotExist:
            pass

        return field_data

class LostPasswordForm(forms.Form):
    username = forms.CharField(label=_("Username"), max_length=30)
    email = forms.EmailField(label=_("E-mail"))

    def clean_username(self):
        # clean old keys when it's requested
        old_keys = LostPassword.objects.filter(key_expires__lt=datetime.date.today())
        for key in old_keys: key.delete()

        field_data = self.cleaned_data['username']

        # control username whether it exists or not
        if len(User.objects.filter(username__iexact=field_data)) == 0:
            raise forms.ValidationError(_("This username is not registered"))

        # control if this user has requested a new password
        if len(LostPassword.objects.filter(user__username__iexact=field_data)) > 0:
            raise forms.ValidationError(_("This username has already requested a new password"))

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
                raise forms.ValidationError(_("This e-mail address is not registered"))
        except User.DoesNotExist:
            pass

        return field_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password_again = forms.CharField(label=_("Password (Again)"), widget=forms.PasswordInput)

    def set_user(self, user):
        self.user = user

    def clean_old_password(self):
        field_data = self.cleaned_data['old_password']

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(_("Password may not contain space character"))

        if len(field_data) > 32:
            raise forms.ValidationError(_("Password must contain less than 32 characters"))

        if len(field_data) < 5:
            raise forms.ValidationError(_("Password must be at least 5 characters long"))

        return field_data

    def clean_password(self):
        field_data = self.cleaned_data['password']

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(_("Password may not contain space character"))

        if len(field_data) > 32:
            raise forms.ValidationError(_("Password must contain less than 32 characters"))

        if len(field_data) < 5:
            raise forms.ValidationError(_("Password must be at least 5 characters long"))

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
                    raise forms.ValidationError(_("Password may not contain space character"))

                if len(field_data) > 32:
                    raise forms.ValidationError(_("Password must contain less than 32 characters"))

                if len(field_data) < 5:
                    raise forms.ValidationError(_("Password must be at least 5 characters long"))

                if (password or field_data) and password != field_data:
                    raise forms.ValidationError(_("Passwords don't match"))

                u = User.objects.get(username=self.user.username)
                if not u.check_password(old_password):
                    raise forms.ValidationError(_("Old password is wrong"))

                return field_data
            else:
                raise forms.ValidationError(_("Fill all of the fields to change password"))
        else:
            return ''

class ResetPasswordForm(forms.Form):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, max_length=32, min_length=5)
    password_again = forms.CharField(label=_("Password (Again)"), widget=forms.PasswordInput, max_length=32, min_length=5)

    def clean_password_again(self):
        field_data = self.cleaned_data['password_again']

        if not self.cleaned_data.has_key('password'):
            return
        else:
            password = self.cleaned_data['password']

        if field_data != password:
            raise forms.ValidationError(_("Passwords don't match"))

        return field_data
