#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.forum.models import Forum, Category, Topic, Post

class ForumAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    prepopulated_fields = {'slug': ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ['-name']
    search_fields = ['name']


class TopicAdmin(admin.ModelAdmin):
    list_display = ("forum", "title")
    ordering = ["-title"]
    search_fields = ["title"]

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "author")
    ordering = ["-id"]
    search_fields = ["text"]

admin.site.register(Forum, ForumAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
