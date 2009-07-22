#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from PIL import Image

from django import forms

from oi.tema.models import *

VALID_WALLPAPER_SIZES = (
    ( 800,  600),
    (1024,  768),
    (1152,  864),
    (1280,  800),
    (1280, 1024),
    (1440,  900),
    (1600, 1200),
    (1680, 1050),
    (1920, 1200),
    (2880, 1800),
)

vote_choices = (
    (0,   '1'),
    (25,  '2'),
    (50,  '3'),
    (75,  '4'),
    (100, '5'),
)

class ThemeItemForm(forms.ModelForm):
    class Meta:
        model = ThemeItem
        exclude = ("parentcategory", "thumbnail", "author", "rating", "download_count", "submit", "update", "status", "slug", "topic")

class ThemeTypeForm(forms.Form):
    category = forms.ChoiceField(label="Kategori", choices=CATEGORIES, help_text="Ekleyeceğiniz içerik için bir kategori seçin")

class WallpaperForm(forms.ModelForm):
    confirmation = forms.BooleanField(label="Onay", required=True, help_text="Bu duvar kağıdını dağıtma hakkına sahibim.")
    class Meta:
        model = Wallpaper
        exclude = ("author", "rating", "category", "thumbnail", "download_count", "submit", "update", "status", "scalable", "papers", "changelog", "slug", "topic", "version")

class WallpaperFileForm(forms.ModelForm):
    create_smaller_wallpapers = forms.BooleanField(label="Küçüklerini Oluştur", required=False, initial=True, help_text="Büyük bir duvar kağıdı gönderiyorsanız bu seçenekle küçüklerinin otomatik oluşturulmasını sağlayabilirsiniz.")

    def clean_image(self):
        image = self.cleaned_data["image"]
        i = Image.open(image)
        if i.size not in VALID_WALLPAPER_SIZES:
            raise forms.ValidationError("%dx%d geçerli bir duvar kağıdı büyüklüğü değil." % i.size)
        return image

    class Meta:
        model = WallpaperFile
        exclude = ("title", "scalable")
