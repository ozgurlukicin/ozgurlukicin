#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

from oi.upload.models import Image
from oi.forum.models import Topic
from oi.forum.tools import create_forum_topic
from oi.st.tags import Tag
from oi.podcast.utils import getDuration
from django.utils.translation import ugettext as _

class Author(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Username"), related_name="podcast_author")

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ['user']
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")

class Episode(models.Model):
    title = models.CharField(_("Title"), max_length=32)
    slug = models.SlugField(_("SEF Title"))
    image = models.ForeignKey(Image, verbose_name=_("Image"), blank=True, null=True)
    sum = models.TextField(_("Summary"))
    text = models.TextField(_("Text"))
    tags = models.ManyToManyField(Tag)
    authors = models.ManyToManyField(Author)
    guests = models.CharField(_("Guests"), blank=True, null=True, max_length=1024)
    minutes = models.IntegerField()
    seconds = models.IntegerField()
    mp3file = models.FileField(upload_to="podcasts/")
    oggfile = models.FileField(upload_to="podcasts/")
    update = models.DateTimeField()
    status = models.BooleanField(_("Active"))
    topic = models.ForeignKey(Topic)

    def __unicode__(self):
        return self.title

    def save(self):
        self.minutes, self.seconds = 0, 0
        create_forum_topic(self, "Ajans Pardus")
        #first save file on disk, second save record duration
        super(Episode, self).save()
        self.minutes, self.seconds = getDuration(self.mp3file.path)
        super(Episode, self).save()

    def get_absolute_url(self):
        return "/podcast/bolum/%s/" % self.slug

    def get_length(self):
        return "%s:%s" % (
            "0%d" % self.minutes if self.minutes<10 else str(self.minutes),
            "0%d" % self.seconds if self.seconds<10 else str(self.seconds)
        )

    def get_guests_list(self):
        return self.guests.split(',')

    class Meta:
        verbose_name = _("Episode")
        verbose_name_plural = _("Episodes")
