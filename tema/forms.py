#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import os, tempfile
from PIL import Image, ImageFont

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
    (1920, 1080),
    (1920, 1200),
    (2880, 1800),
)

RATINGS = (
    (0.5, 'çok kötü'),
    (1, 'çok kötü'),
    (1.5, 'kötü'),
    (2, 'kötü'),
    (2.5, 'iyi'),
    (3, 'iyi'),
    (3.5, 'çok iyi'),
    (4, 'çok iyi'),
    (4.5, 'harika'),
    (5, 'harika'),
)

class ThemeItemForm(forms.ModelForm):
    class Meta:
        model = ThemeItem
        exclude = ("parentcategory", "thumbnail", "author", "rating", "download_count", "submit", "update", "status", "slug", "topic")

class ThemeTypeForm(forms.Form):
    category = forms.ChoiceField(label="Kategori", choices=CATEGORIES, help_text="Ekleyeceğiniz içerik için bir kategori seçin")

class FontForm(forms.ModelForm):
    text = forms.CharField(label="Tanım", required=True, help_text="Ekleyeceğiniz dosyalar hakkındaki açıklamalarınızı bu bölümde belirtebilirsiniz.", widget=forms.Textarea(attrs={"style":"width:400px"}))
    confirmation = forms.BooleanField(label="Onay", required=True, help_text="Bu yazıtipini dağıtma hakkına sahibim.")
    license = forms.ModelChoiceField(label="Lisans", queryset=License.objects.order_by("name"), empty_label="---------")
    origin_url = forms.URLField(label="Web Sitesi", required=True, help_text="Yazıtipi üreticisinin web sitesi.", widget=forms.TextInput(attrs={"style":"width:400px"}))

    class Meta:
        model = Font
        exclude = ("author", "rating", "category", "thumbnail", "download_count", "submit", "update", "status", "scalable", "changelog", "slug", "topic")

    def clean_tags(self):
        field_data = self.cleaned_data['tags']
        if len(field_data) > 5:
            raise forms.ValidationError("En fazla 5 etiket seçebilirsiniz. Lütfen açtığınız başlığa uygun etiket seçiniz.")
        return field_data

    def clean_font(self):
        font = self.cleaned_data["font"]
        if font:
            handle, tmp = tempfile.mkstemp()
            file = open(tmp, "w")
            file.write(font.read())
            file.close()
            try:
                ImageFont.truetype(tmp, 22)
            except IOError:
                os.unlink(tmp)
                raise forms.ValidationError("Gönderdiğiniz yazıtipi okunamadı.")
            os.unlink(tmp)
        return font


class DesktopScreenShotForm(forms.ModelForm):
    text = forms.CharField(label="Tanım", required=True, help_text="Ekleyeceğiniz dosyalar hakkındaki açıklamalarınızı bu bölümde belirtebilirsiniz.", widget=forms.Textarea(attrs={"style":"width:400px"}))
    confirmation = forms.BooleanField(label="Onay", required=True, help_text="Bu ekran görüntüsünü dağıtma hakkına sahibim.")
    license = forms.ModelChoiceField(label="Lisans", queryset=License.objects.order_by("name"), empty_label="---------")
    origin_url = forms.URLField(label="Özgün Çalışma", required=True, help_text="Başka bir çalışmayı temel aldıysanız bunun bağlantısını yazın.", widget=forms.TextInput(attrs={"style":"width:400px"}))

    class Meta:
        model = DesktopScreenshot
        exclude = ("author", "rating", "category", "thumbnail", "download_count", "submit", "update", "status", "scalable", "papers", "changelog", "slug", "topic", "version")

    def clean_tags(self):
        field_data = self.cleaned_data['tags']
        if len(field_data) > 5:
            raise forms.ValidationError("En fazla 5 etiket seçebilirsiniz. Lütfen açtığınız başlığa uygun etiket seçiniz.")
        return field_data


class WallpaperForm(forms.ModelForm):
    text = forms.CharField(label="Tanım", required=True, help_text="Ekleyeceğiniz dosyalar hakkındaki açıklamalarınızı bu bölümde belirtebilirsiniz.", widget=forms.Textarea(attrs={"style":"width:400px"}))
    confirmation = forms.BooleanField(label="Onay", required=True, help_text="Bu duvar kağıdını dağıtma hakkına sahibim.")
    license = forms.ModelChoiceField(label="Lisans", queryset=License.objects.order_by("name"), empty_label="---------")
    origin_url = forms.URLField(label="Özgün Çalışma", required=True, help_text="Başka bir çalışmayı temel aldıysanız bunun bağlantısını yazın.", widget=forms.TextInput(attrs={"style":"width:400px"}))

    class Meta:
        model = Wallpaper
        exclude = ("author", "rating", "category", "thumbnail", "download_count", "submit", "update", "status", "scalable", "papers", "changelog", "slug", "topic", "version")

    def clean_tags(self):
        field_data = self.cleaned_data['tags']
        if len(field_data) > 5:
            raise forms.ValidationError("En fazla 5 etiket seçebilirsiniz. Lütfen açtığınız başlığa uygun etiket seçiniz.")
        return field_data

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

class ThemeRatingForm(forms.Form):
    rating = forms.ChoiceField(choices=RATINGS)
