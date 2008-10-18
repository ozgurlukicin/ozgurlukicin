#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.profile.models import ForbiddenUsername, Avatar, LostPassword, Profile

class ForbiddenUsernameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['-name']
    search_fields = ['name']

class AvatarAdmin(admin.ModelAdmin):
    list_display = ("name", "file")
    ordering = ["name"]
    search_fields = ["name", "file"]

class LostPasswordAdmin(admin.ModelAdmin):
    fieldsets = (
        ('foo', {'fields': ('user', 'key', 'key_expires'),}),
        )
    list_display = ('user', 'key', 'key_expires',)
    ordering = ['-user']

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Üyelik Bilgileri', {'fields': ('user', 'avatar', 'homepage', 'msn', 'jabber', 'icq', 'city', 'birthday', 'contributes', 'contributes_summary', 'show_email', 'latitude', 'longitude',)}),
        ('Diğer', {'fields': ('activation_key', 'key_expires', 'signature'), 'classes': 'collapse',}),
    )

    list_display = ('user', 'city',)
    ordering = ['-user']
    search_fields = ['user__username']

admin.site.register(ForbiddenUsername, ForbiddenUsernameAdmin)
admin.site.register(Avatar, AvatarAdmin)
admin.site.register(LostPassword, LostPasswordAdmin)
admin.site.register(Profile, ProfileAdmin)
