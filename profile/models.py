#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007, 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re, random, datetime
try:
    from hashlib import sha1 as sha
except ImportError:
    import sha

from django.db import models
from django.contrib.auth.models import User
from django import forms

from oi.middleware import threadlocals
from oi.settings import CITY_LIST
from oi.st.models import Contribute

from oi.shop.shopprofile.models import ShopProfile

PARDUS_VERSIONS = (
    (0, "---"),
    (4,"Pardus 2009"),
    (3,"Pardus 2008"),
    (2,"Pardus 2007"),
    (1,"Pardus 1.0"),
)

class ForbiddenUsername(models.Model):
    name = models.CharField("Kullanıcı adı", max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Yasaklanan Kullanıcı Adı"
        verbose_name_plural = "Yasaklanan Kullanıcı Adları"

class Avatar(models.Model):
    name = models.CharField("Açıklama", max_length=32, unique=True)
    file = models.ImageField(upload_to="avatar/")

    def __unicode__(self):
        return unicode(self.file)

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatarlar"

class LostPassword(models.Model):
    user = models.ForeignKey(User, verbose_name='Kullanıcı')
    key = models.CharField('Anahtar', max_length=40, unique=True)
    key_expires = models.DateTimeField('Zaman Aşımı')

    def __unicode__(self):
        return "%s" % self.key

    def is_expired(self):
        if datetime.datetime.today() > self.key_expires:
            return True
        else:
            return False

    class Meta:
        verbose_name = "Kayıp Parola"
        verbose_name_plural = "Kayıp Parolalar"

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    title = models.CharField("Ünvan", max_length=32, blank=True, help_text="'Forum Yöneticisi' gibi")
    avatar = models.ForeignKey(Avatar, verbose_name="Avatar")
    birthday = models.DateField(blank=True)
    homepage = models.URLField('Ana Sayfa', blank=True, verify_exists=False, unique=False)
    msn = models.EmailField('MSN', max_length=50, blank=True)
    jabber = models.EmailField('Jabber', max_length=50, blank=True)
    icq = models.CharField('ICQ', max_length=15, blank=True)
    city = models.CharField('Şehir', blank=True, choices=CITY_LIST, max_length=40)
    pardus_version = models.IntegerField(blank=True, null=True, choices=PARDUS_VERSIONS)
    show_email = models.BooleanField('E-posta Göster', default=0)
    show_birthday = models.BooleanField('Doğum Tarihini Göster', default=0)
    contributes = models.ManyToManyField(Contribute, blank=True, verbose_name='Katkılar')
    contributes_summary = models.TextField('Katkı Açıklaması', blank=True)
    bio = models.TextField("Kendinizi Tanıtın", blank=True)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    signature = models.TextField('İmza', blank=True, max_length=512)
    latitude = models.DecimalField('Enlem', max_digits=10, decimal_places=6, default=0)
    longitude = models.DecimalField('Boylam', max_digits=10, decimal_places=6, default=0)

    def have_shopprofile(self):
        # helper method for checking if the user has created shop profile
        if ShopProfile.objects.filter(user=self.user).count() > 0:
            return True
        else:
            return False

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"

    def get_absolute_url(self):
        return '/kullanici/profil/%s/' % self.user.username

    def get_theme_content_url(self):
        return "/tema/kullanici/%s/" % self.user.username
