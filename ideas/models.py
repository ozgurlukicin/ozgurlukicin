#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from django.db import models
from django.contrib.auth.models import User
from oi.st.tags import Tag
from oi.forum.models import Topic
from django.utils.translation import ugettext as _


class StatusCategory(models.Model):
    name = models.CharField(_("Name"), max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Status Category")
        verbose_name_plural = _("Status Categories")

class Status(models.Model):
    category = models.ForeignKey(StatusCategory, verbose_name = "_(Status Category)")
    name = models.CharField(_("Name"), max_length = 128)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    slug = models.SlugField(_("SEF name"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return "/yenifikir/listele/kategori/%s/" % self.slug

class RelatedCategory(models.Model):
    name = models.CharField(_("Name"), max_length=150)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Related Category")
        verbose_name_plural = _("Related Categories")

class Related(models.Model):
    category = models.ForeignKey(RelatedCategory, verbose_name = _("Category"))
    name = models.CharField(_("Name"), max_length=150)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Related")
        verbose_name_plural = _("Relateds")


class Idea(models.Model):
    title = models.CharField(_("Title"), help_text=_("Idea title"), max_length=100)
    submitted_date = models.DateTimeField(_("Date"), auto_now_add=True)
    submitter = models.ForeignKey(User, verbose_name=_("Submitter"))
    description = models.TextField(_("Description"), help_text=_("Explain your idea here."))
    status = models.ForeignKey(Status,verbose_name=_("Status"))
    category = models.ForeignKey(Category, null=True, verbose_name=_("Category"))
    related_to = models.ForeignKey(Related, blank=True, null=True, verbose_name=_("Related to this"), help_text=_("You may leave this field blank."))
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"))
    vote_count = models.IntegerField(_("Vote count"), default=0)
    duplicate = models.ForeignKey("self", blank=True, null=True, verbose_name=_("Duplicate"))
    is_duplicate = models.BooleanField(_("Is duplicate"), default=False)
    forum_url = models.URLField(_("Related forum address"), help_text=_("Write related forum address if it exists."), blank=True)
    bug_numbers = models.CharField(_("Bug Numbers"), help_text=_("Enter related bug numbers seperated my commasi if exists. Example: 123, 562"), max_length=63, blank=True)
    file = models.FileField(upload_to="upload/ideas/dosya/", blank=True, verbose_name=_("File"))
    is_hidden = models.BooleanField(_("Hidden"), default=False)
    topic = models.ForeignKey(Topic, verbose_name=_("Forum topic for this idea"))

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/yenifikir/ayrinti/%s/" % self.id

    class Meta:
        verbose_name = _("New Idea")
        verbose_name_plural = _("New Ideas")

class Vote(models.Model):
    idea = models.ForeignKey(Idea, verbose_name=_("Voted idea"), related_name="vote_idea", blank=False, null=False)
    user = models.ForeignKey(User, verbose_name=_("Voter"), related_name="vote_author", blank=False, null=False)
    vote = models.IntegerField(_("Vote"), blank=False)

    def __unicode__(self):
        return self.idea

    class Meta:
        unique_together = ("idea", "user")
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")

class Favorite(models.Model):
    user = models.ForeignKey(User, verbose_name = _("User"), related_name="fav_author", blank=False)
    idea = models.ForeignKey(Idea, verbose_name = _("Favourite"), related_name="fav_idea", blank=False)

    def __unicode__(self):
        return self.idea

    class Meta:
        verbose_name = _("Favourite")
        verbose_name_plural = _("Favourites")
