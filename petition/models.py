#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django import forms
from django.contrib import admin

from oi.settings import CITY_LIST

from django.utils.translation import ugettext as _

class Petitioner(models.Model):
    firstname = models.CharField(_("Name"), max_length=30)
    lastname = models.CharField(_("Surname"), max_length=30)
    city = models.CharField(_("City"), blank=True, choices=CITY_LIST, max_length=40)
    job = models.CharField(_("Job"), max_length=30)
    email = models.EmailField(_("E-mail"), max_length=50)
    homepage = models.URLField(_("Mainpage"), blank=True, verify_exists=False, unique=False)
    signed = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=_("Sign date"))
    activation_key = models.CharField(_("Activation Key"), max_length=40)
    is_active = models.BooleanField(_("Active"))
    inform = models.BooleanField(_("Inform"))

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)

    class Meta:
        verbose_name = _("Signer")
        verbose_name_plural = _("Signers")

class PetitionerAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "job", "city", "email", "homepage", "signed", "is_active", "inform")
    ordering = ("-signed",)
    search_fields = ("firstname", "lastname", "job")

admin.site.register(Petitioner, PetitionerAdmin)

class PetitionForm(forms.Form):
    firstname = forms.CharField(label=_("Name"), max_length=30)
    lastname = forms.CharField(label=_("Surname"), max_length=30)
    city = forms.ChoiceField(label=_("City"), choices=CITY_LIST)
    job = forms.CharField(label=_("Job"), max_length=30)
    email = forms.EmailField(label=_("E-Mail"))
    homepage = forms.URLField(label=_("Web Site"), verify_exists=False, required=False, help_text=_("(not required)"))
    inform = forms.BooleanField(label=_("Inform me about events:"), required=False, help_text=_("Select this if you want to get news about other Spread Pardus events."))

    def clean_email(self):
        field_data = self.cleaned_data["email"]

        if not field_data:
            return ''

        u = Petitioner.objects.filter(email=field_data)
        if len(u) > 0:
            raise forms.ValidationError(_("This e-mail address has already signed the petition."))

        return field_data
