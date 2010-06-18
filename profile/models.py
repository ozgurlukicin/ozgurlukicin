#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007, 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime
import random
import re

from django.db import models
from django.contrib.auth.models import User
from django import forms

from oi.middleware import threadlocals
from oi.settings import CITY_LIST
from oi.st.models import Contribute
from oi.shop.shopprofile.models import ShopProfile
from django.utils.translation import ugettext as _

PARDUS_VERSIONS = (
    (0, "---"),
    (4,"Pardus 2009"),
    (3,"Pardus 2008"),
    (2,"Pardus 2007"),
    (1,"Pardus 1.0"),
)

class ForbiddenUsername(models.Model):
    name = models.CharField(_("Username"), max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Forbidden Username")
        verbose_name_plural = _("Forbidden Usernames")

class Avatar(models.Model):
    name = models.CharField(_("Name"), max_length=32, unique=True)
    file = models.ImageField(upload_to="avatar/")

    def __unicode__(self):
        return unicode(self.file)

    class Meta:
        verbose_name = _("Avatar")
        verbose_name_plural = _("Avatars")

class LostPassword(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"))
    key = models.CharField(_("Key"), max_length=40, unique=True)
    key_expires = models.DateTimeField(_("Timeout"))

    def __unicode__(self):
        return "%s" % self.key

    def is_expired(self):
        if datetime.datetime.today() > self.key_expires:
            return True
        else:
            return False

    class Meta:
        verbose_name = _("Lost Password")
        verbose_name_plural = _("Lost Passwords")

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    title = models.CharField(_("Title"), max_length=32, blank=True, help_text=_("example: 'Forum Moderator'"))
    avatar = models.ForeignKey(Avatar, verbose_name=_("Avatar"))
    birthday = models.DateField(blank=True)
    homepage = models.URLField(_("Web Page"), blank=True, verify_exists=False, unique=False)
    msn = models.EmailField('MSN', max_length=50, blank=True)
    jabber = models.EmailField('Jabber', max_length=50, blank=True)
    icq = models.CharField('ICQ', max_length=15, blank=True)
    city = models.CharField(_("City"), blank=True, choices=CITY_LIST, max_length=40)
    pardus_version = models.IntegerField(blank=True, null=True, choices=PARDUS_VERSIONS)
    show_email = models.BooleanField(_("Show e-mail address"), default=False)
    show_birthday = models.BooleanField(_("Show birth date"), default=False)
    contributes = models.ManyToManyField(Contribute, blank=True, verbose_name=_("Contributions"))
    contributes_summary = models.TextField(_("Contribution Comment"), blank=True)
    bio = models.TextField(_("Introduce yourself"), blank=True)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    signature = models.TextField(_("Signature"), blank=True, max_length=512)
    latitude = models.DecimalField(_("Latitude"), max_digits=10, decimal_places=6, default=0)
    longitude = models.DecimalField(_("Longitude"), max_digits=10, decimal_places=6, default=0)

    def have_shopprofile(self):
        # helper method for checking if the user has created shop profile
        if ShopProfile.objects.filter(user=self.user).count() > 0:
            return True
        else:
            return False

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def get_absolute_url(self):
        return '/kullanici/profil/%s/' % self.user.username

    def get_theme_content_url(self):
        return "/tema/kullanici/%s/" % self.user.username
