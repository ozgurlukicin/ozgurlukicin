#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import template
from django.template import Context, loader
from oi.tema.models import ThemeItem, ThemeAbuseReport, DesktopScreenshot, Wallpaper, Font

register = template.Library()

@register.simple_tag
def number_of_theme_abuse():
    return ThemeAbuseReport.objects.count()

@register.simple_tag
def top_content(category=None):
    if category == "duvar-kagitlari":
        object_list = Wallpaper.objects.all()
        title = "En Beğenilen Duvar Kağıtları"
    elif category == "masaustu-goruntuleri":
        object_list = DesktopScreenshot.objects.all()
        title = "En Beğenilen Masaüstleri"
    elif category == "yazitipleri":
        object_list = Font.objects.all()
        title = "En Beğenilen Yazıtipleri"
    else:
        object_list = ThemeItem.objects.all()
        title = "En Çok Beğenilenler"
    object_list = object_list.filter(status=True).order_by("-rating", "-update")[:10]
    return loader.get_template("tema/sidebar.html").render(Context({"object_list":object_list,"title":title}))
