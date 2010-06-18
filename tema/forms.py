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

from django.utils.translation import ugettext as _

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
    (0.5, _('very bad')),
    (1, _('very bad')),
    (1.5, _('bad')),
    (2, _('bad')),
    (2.5, _('good')),
    (3, _('good')),
    (3.5, _('very good')),
    (4, _('very good')),
    (4.5, _('excellent')),
    (5, _('excellent')),
)

class ThemeItemForm(forms.ModelForm):
    class Meta:
        model = ThemeItem
        exclude = ("parentcategory", "thumbnail", "author", "rating",
                "download_count", "submit", "update", "status", "deny_reason", "slug", "topic")

class ThemeTypeForm(forms.Form):
    category = forms.ChoiceField(label=_("Category"), choices=CATEGORIES, help_text=_("Choose a category for your content"))

class FontForm(forms.ModelForm):
    text = forms.CharField(label=_("Description"), required=True, help_text=_("You can specify your description about the files you submitted here."), widget=forms.Textarea(attrs={"style":"width:400px"}))
    confirmation = forms.BooleanField(label=_("Confirmation"), required=True, help_text=_("I have the right to give this font away to everyone."))
    license = forms.ModelChoiceField(label=_("License"), queryset=License.objects.order_by("name"), empty_label="---------")
    origin_url = forms.URLField(label=_("Web Site"), required=True, help_text=_("Web site of font maker."), widget=forms.TextInput(attrs={"style":"width:400px"}))

    class Meta:
        model = Font
        exclude = ("author", "rating", "category", "thumbnail",
                "download_count", "submit", "update", "status", "deny_reason", "scalable", "changelog", "slug", "topic")

    def clean_tags(self):
        field_data = self.cleaned_data['tags']
        if len(field_data) > 5:
            raise forms.ValidationError(_("You can choose 5 tags at most. Please choose only relevant tags with your topic."))
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
                raise forms.ValidationError(_("Your font couldn't be read."))
            os.unlink(tmp)
        return font


class DesktopScreenShotForm(forms.ModelForm):
    text = forms.CharField(label=_("Description"), required=True, help_text=_("You can specify your description about the files you submitted here."), widget=forms.Textarea(attrs={"style":"width:400px"}))
    confirmation = forms.BooleanField(label=_("Confirmation"), required=True, help_text=_("I have the right to give this screenshot away to everyone."))
    license = forms.ModelChoiceField(label=_("License"), queryset=License.objects.order_by("name"), empty_label="---------")
    origin_url = forms.URLField(label=_("Original Work"), required=False, help_text=_("Link to original work if exists."), widget=forms.TextInput(attrs={"style":"width:400px"}))

    class Meta:
        model = DesktopScreenshot
        exclude = ("author", "rating", "category", "thumbnail",
                "download_count", "submit", "update", "status", "deny_reason", "scalable", "papers", "changelog", "slug", "topic", "version")

    def clean_tags(self):
        field_data = self.cleaned_data['tags']
        if len(field_data) > 5:
            raise forms.ValidationError(_("You can choose 5 tags at most. Please choose only relevant tags with your topic."))
        return field_data


class WallpaperForm(forms.ModelForm):
    text = forms.CharField(label=_("Description"), required=True, help_text=_("You can specify your description about the files you submitted here."), widget=forms.Textarea(attrs={"style":"width:400px"}))
    confirmation = forms.BooleanField(label=_("Confirmation"), required=True, help_text=_("I have the right to give this wallpaper away to everyone."))
    license = forms.ModelChoiceField(label=_("License"), queryset=License.objects.order_by("name"), empty_label="---------")
    origin_url = forms.URLField(label=_("Original Work"), required=False, help_text=_("Link to original work if exists."), widget=forms.TextInput(attrs={"style":"width:400px"}))

    class Meta:
        model = Wallpaper
        exclude = ("author", "rating", "category", "thumbnail",
                "download_count", "submit", "update", "status", "deny_reason" , "scalable", "papers", "changelog", "slug", "topic", "version")

    def clean_tags(self):
        field_data = self.cleaned_data['tags']
        if len(field_data) > 5:
            raise forms.ValidationError(_("You can choose 5 tags at most. Please choose only relevant tags with your topic."))
        return field_data

class WallpaperFileForm(forms.ModelForm):
    create_smaller_wallpapers = forms.BooleanField(label=_("Create Smaller Wallpapers"), required=False, initial=True, help_text="If you're sending a large wallpaper, this option will create smallers ones automaticly.")

    def clean_image(self):
        image = self.cleaned_data["image"]
        i = Image.open(image)
        if i.size not in VALID_WALLPAPER_SIZES:
            raise forms.ValidationError(_("%(size)s is not a valid wallpaper size.") % {"size": "%dx%d" % i.size})
        return image

    class Meta:
        model = WallpaperFile
        exclude = ("title", "scalable")

class ThemeRatingForm(forms.Form):
    rating = forms.ChoiceField(choices=RATINGS)
