#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007, 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext as _

class Place(models.Model):
    name = models.CharField(_("Seminar Location"), max_length=64, blank=False, unique=True)
    description = models.TextField(_("Location Description"), max_length=512, blank=True)
    phone = models.CharField(_("Telephone"), max_length=16, blank=True)
    latitude = models.DecimalField(_("Latitude"), max_digits=10, decimal_places=6, default=0, help_text=_("like 40.903823"))
    longitude = models.DecimalField(_("Longitude"), max_digits=10, decimal_places=6, default=0, help_text=_("like 29.226723"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("Seminar Location")
        verbose_name_plural = _("Seminar Locations")

class Attender(models.Model):
    name = models.CharField(_("Real Name"), max_length=64, blank=False, unique=True)
    user = models.ForeignKey(User, verbose_name=_("Username"), blank=True, null=True, help_text=_("Not required"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")

class Seminar(models.Model):
    description = models.CharField(_("Seminar description"), max_length = 64, blank = False)
    place = models.ForeignKey(Place, verbose_name=_("Location"))
    attender = models.ManyToManyField(Attender, verbose_name=_("Attenders"))
    start_date = models.DateTimeField(_("Start date"), blank=False)
    end_date = models.DateTimeField(_("End date"), blank=True, null=True, help_text=_("Not required"))
    status = models.BooleanField(_("Active"))

    def __unicode__(self):
        return self.description

    def get_absolute_url(self):
        return "/seminer/%d/" % self.id

    class Meta:
        verbose_name = _("Seminar")
        verbose_name_plural = _("Seminars")
