#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from oi.settings import WEB_URL
from django.utils.translation import ugettext as _

STATUS_CODES = (
    (1, _("New")),
    (2, _("Assigned")),
    (3, _("Closed")),
    )
PRIORITIES = (
    (1, _("Preventive")),
    (2, _("Important")),
    (3, _("Normal")),
    (4, _("Unimportant")),
    (5, _("Improvement")),
    )

class Bug(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    submitted_date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    submitter = models.ForeignKey(User, verbose_name=_("Sender"), related_name="submitter")
    assigned_to = models.ForeignKey(User, verbose_name=_("Assignee"))
    description = models.TextField(verbose_name=_("Description"), blank=False)
    status = models.IntegerField(verbose_name=_("Status"), default=1, choices=STATUS_CODES)
    priority = models.IntegerField(verbose_name=_("Priority"), default=3, choices=PRIORITIES)

    def __unicode__(self):
        return self.title

    def get_full_url(self):
        return "%s%s" % (WEB_URL, self.get_absolute_url())

    def get_absolute_url(self):
        return "/hata/%s/" % self.id

    class Admin:
        list_display = ('status', 'title', 'submitter', 'assigned_to')
        list_filter = ('status', 'submitted_date')
        search_fields = ('assigned_to', 'submitter', 'title', 'description')

class Comment(models.Model):
    bug = models.ForeignKey(Bug, verbose_name=_("Bug"))
    author = models.ForeignKey(User, verbose_name=_("Author"))
    text = models.TextField(blank=False, verbose_name=_("Comment"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    def __unicode__(self):
        return self.text

    class Admin:
        list_display = ('bug', 'author')
        list_filter = ('bug', 'date')
        search_fields = ('text', 'submitter')
