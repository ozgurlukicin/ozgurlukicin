#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re, random, datetime, sha

from django.db import models
from django.contrib.auth.models import User
from django import newforms as forms

from oi.middleware import threadlocals
from oi.settings import CITY_LIST
from oi.st.models import Contribute

class ForbiddenUsername(models.Model):
    name = models.CharField("Kullanıcı adı", max_length=30)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name',)
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        verbose_name = "Yasaklanan Kullanıcı Adı"
        verbose_name_plural = "Yasaklanan Kullanıcı Adları"

class Avatar(models.Model):
    name = models.CharField("Açıklama", max_length=32, unique=True)
    file = models.ImageField(upload_to="avatar/")

    def __str__(self):
        return self.file

    class Admin:
        list_display = ("name", "file")
        ordering = ["name"]
        search_fields = ["name", "file"]

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatarlar"

class LostPassword(models.Model):
    user = models.ForeignKey(User, verbose_name='Kullanıcı')
    key = models.CharField('Anahtar', max_length=40, unique=True)
    key_expires = models.DateTimeField('Zaman Aşımı')

    def __str__(self):
        return "%s" % self.key

    def is_expired(self):
        if datetime.datetime.today() > self.key_expires:
            return True
        else:
            return False

    class Meta:
        verbose_name = "Kayıp Parola"
        verbose_name_plural = "Kayıp Parolalar"

    class Admin:
        fields = (
            ('foo', {'fields': ('user', 'key', 'key_expires'),}),
            )
        list_display = ('user', 'key', 'key_expires',)
        ordering = ['-user']

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    avatar = models.ForeignKey(Avatar, verbose_name="Avatar")
    birthday = models.DateField(blank=True)
    homepage = models.URLField('Ana Sayfa', blank=True, verify_exists=False, unique=False)
    msn = models.EmailField('MSN', max_length=50, blank=True)
    jabber = models.EmailField('Jabber', max_length=50, blank=True)
    icq = models.EmailField('ICQ', max_length=50, blank=True)
    city = models.CharField('Şehir', blank=True, choices=CITY_LIST, max_length=40)
    show_email = models.BooleanField('E-posta Göster', default=0)
    contributes = models.ManyToManyField(Contribute, blank=True, verbose_name='Katkılar')
    contributes_summary = models.TextField('Katkı Açıklaması', blank=True)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    signature = models.TextField('İmza', blank=True)

    def __str__(self):
        return self.user.username

    class Admin:
        fields = (
            ('Üyelik Bilgileri', {'fields': ('user', 'avatar', 'homepage', 'msn', 'city', 'birthday', 'contributes', 'contributes_summary', 'show_email',)}),
            ('Diğer', {'fields': ('activation_key', 'key_expires', 'signature'), 'classes': 'collapse',}),
        )

        list_display = ('user', 'city',)
        ordering = ['-user']
        search_fields = ['user']

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"
