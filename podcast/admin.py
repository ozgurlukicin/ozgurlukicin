#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.podcast.models import *

class EpisodeAdmin(admin.ModelAdmin):
    exclude = ("topic", "minutes", "seconds")
    class Media:
        js = ("admin/tinymce/jscripts/tiny_mce/tiny_mce.js", "js/tinymce_setup.js", "js/jquery-1.4.2.min.js", "js/adminimages.js", "js/jquery.autocomplete.js", "js/taghelper.js")
        css = {
                "all": ("media/admin/css/jquery-ui-grappelli-extensions.css",),
        }

admin.site.register(Author)
admin.site.register(Episode, EpisodeAdmin)
