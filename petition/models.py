#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Uğur Çetin
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django import newforms as forms

from oi.settings import CITY_LIST

class Petitioner(models.Model):
    firstname = models.CharField("Ad", maxlength=30)
    lastname = models.CharField("Soyad", maxlength=30)
    city = models.CharField("Şehir", blank=True, choices=CITY_LIST, maxlength=40)
    job = models.CharField("Meslek", maxlength=30)
    email = models.EmailField("E-posta", maxlength=50)
    homepage = models.URLField("Ana Sayfa", blank=True, verify_exists=False, unique=False)
    signed = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name='İmzalama tarihi')
    activation_key = models.CharField("Etkinleştirme Anahtarı", maxlength=40)
    is_active = models.BooleanField("Etkin")

    def __str__(self):
        return "%s %s" % (self.firstname, self.lastname)

    class Admin:
        list_display = ("firstname", "lastname", "job", "city", "email", "homepage", "signed", "activation_key", "is_active")
        ordering = ["-signed"]
        search_fields = ["firstname", "lastname", "job"]

    class Meta:
        verbose_name = "İmzalayan"
        verbose_name_plural = "İmzalayanlar"

class PetitionForm(forms.Form):
    firstname = forms.CharField(label="Ad", max_length=30)
    lastname = forms.CharField(label="Soyad", max_length=30)
    city = forms.ChoiceField(label="Şehir", choices=CITY_LIST)
    job = forms.CharField(label="Meslek", max_length=30)
    email = forms.EmailField(label="E-Posta")
    homepage = forms.URLField(label="Web Sayfası", verify_exists=False, required=False, help_text='(zorunlu değil)')

    def clean_email(self):
        field_data = self.clean_data["email"]

        if not field_data:
            return ''

        u = Petitioner.objects.filter(email=field_data)
        if len(u) > 0:
            raise forms.ValidationError(u"Bu e-posta adresi ile daha önceden kayıt yapılmış")

        return field_data
