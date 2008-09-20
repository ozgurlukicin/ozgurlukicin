#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.ideas.models import StatusCategory, Status, Category, RelatedCategory, Related, Idea, Vote, Favorite
from oi.st.tags import Tag

class StatusCategoryAdmin(admin.ModelAdmin):
    list_display = ('name')

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}

claspass
    list_display = ('name')

class RelatedAdmin(admin.ModelAdmin):
    list_display = ('name')

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'submitter', 'submitted_date', 'category', 'related_to', 'is_hidden', 'is_duplicate', 'duplicate')
    list_filter = ('status', 'is_hidden', 'is_duplicate',  'category', 'related_to')

class VoteAdmin(admin.ModelAdmin):
    pass

class FavoriteAdmin(admin.ModelAdmin):
    pass

admin.site.register(StatusCategory, StatusCategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(RelatedCategory, RelatedCategoryAdmin)
admin.site.register(Related, RelatedAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Favorite, FavoriteAdmin)
