#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

STATUS_CODES = (
    (1, 'Open'),
    (2, 'Working'),
    (3, 'Closed'),
    )

class Bug(models.Model):
    title = models.CharField(maxlength=100)
    submitted_date = models.DateField(auto_now_add=True)
    submitter = models.ForeignKey(User, related_name="submitter")
    assigned_to = models.ForeignKey(User)
    description = models.TextField(blank=False)
    status = models.IntegerField(default=1, choices=STATUS_CODES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/bug/%s/" % self.id

    class Admin:
        list_display = ('status', 'title', 'submitter', 'assigned_to')
        list_filter = ('status', 'submitted_date')
        search_fields = ('assigned_to', 'submitter', 'title', 'description')
