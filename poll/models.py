#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class PollVote(models.Model):
    poll = models.ForeignKey("Poll", verbose_name=_("Poll"))
    option = models.ForeignKey("PollOption", verbose_name=_("Option"))
    voter = models.ForeignKey(User)
    voter_ip = models.IPAddressField(blank=True, verbose_name=_("IP Address"))

    def __unicode__(self):
        return self.option.__unicode__()

    class Admin:
        list_display = ("option", "voter", "voter_ip")
        ordering = ["option"]
        search_fields = ["voter_ip"]

class PollOption(models.Model):
    poll = models.ForeignKey("Poll", verbose_name=_("Poll"))
    text = models.CharField(_("Text"), max_length=128)
    vote_count = models.IntegerField(default=0)

    def __unicode__(self):
        if len(self.text) > 32:
            return "%s..." % self.question[:30]
        else:
            return self.text

    class Admin:
        list_display = ("poll", "text", "vote_count")
        ordering = ["poll"]
        search_fields = ["text"]

class Poll(models.Model):
    question = models.CharField(_("Question"), max_length=128)
    allow_changing_vote = models.BooleanField(_("Changing vote is allowed"), default=False, blank=True, help_text=_("Check this if you want users to be able to change votes after casting."))
    allow_multiple_choices = models.BooleanField(_("Multiple options allowed"), default=False, blank=True, help_text=_("Check this if you want users to be able to cast votes on multiple options. Warning: You can't change this option later."))
    date_limit = models.BooleanField(_("Timed"), help_text=_("Check this if you want voting to end at a specified date."))
    end_date = models.DateTimeField(_("End Date"), blank=True, null=True, help_text=_("Specify when vote casting will be disabled. like 30/8/2008."))
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=_('Creation Date'))

    def __unicode__(self):
        if len(self.question) > 32:
            return "%s..." % self.question[:30]
        else:
            return self.question

    class Admin:
        list_display = ("question", "allow_changing_vote", "date_limit", "end_date", "created")
        search_fields = ["question"]

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")
