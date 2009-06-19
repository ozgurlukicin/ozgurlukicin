#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import forms

from oi.tema.models import *

vote_choices=(
    (0,   '1'),
    (25,  '2'),
    (50,  '3'),
    (75,  '4'),
    (100, '5'),
)

class ThemeItemForm(forms.ModelForm):
    class Meta:
        model = ThemeItem
        exclude = ("parentcategory", "thumbnail", "author", "rating", "download_count", "submit", "update", "status", "slug")

class ThemeTypeForm(forms.Form):
    category = forms.ChoiceField(label="Kategori", choices=CATEGORIES)

class WallpaperForm(forms.ModelForm):
    class Meta:
        model = Wallpaper
        exclude = ("author", "rating", "category", "thumbnail", "download_count", "submit", "update", "status", "scalable", "papers", "changelog", "slug")

class WallpaperFileForm(forms.ModelForm):
    create_thumbs = forms.BooleanField(label="Küçüklerini Oluştur", required=False, initial=True, help_text="Büyük bir duvar kağıdı gönderiyorsanız bu seçenekle küçüklerinin otomatik oluşturulmasını sağlayabilirsiniz.")
    class Meta:
        model = WallpaperFile
        exclude = ("scalable",)
