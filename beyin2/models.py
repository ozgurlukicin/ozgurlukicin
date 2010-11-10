#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from oi.forum.models import Topic
from oi.st.tags import Tag
# Create your models here.
import os

voteChoices = (
            ( 'U', '+1'),
            ( 'D', '-1'),
            ( 'N', ' 0'),
)

class Idea(models.Model):
    title = models.CharField(max_length = 512, verbose_name = "Başlık")
    description = models.TextField(verbose_name = "Açıklama")
    dateSubmitted = models.DateTimeField("date submitted", default=datetime.now())
    submitter = models.ForeignKey(User, related_name="idea_submitter")
    status = models.ForeignKey("Status", blank=True, null=True, verbose_name = "Durum")
    category = models.ForeignKey("Category", blank=True, null=True, verbose_name = "Kategori")
    duplicate = models.ForeignKey("self", blank=True, null=True)
    is_duplicate = models.BooleanField("Idea Duplicate", default=False)
    is_hidden = models.BooleanField("Hiddden", default=False)
    topic = models.ForeignKey(Topic, related_name="Idea_topic")
    tags = models.ManyToManyField(Tag, blank=True, null=True, verbose_name = "Etiketler")
    # percent will be processed as %UUU,%NNN %DDD
    vote_percent = models.IntegerField(default=0)
    vote_value = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/beyin2/%s/detail/" % self.id

    def get_duplications(self):
        return Idea.objects.filter(duplicate=self)

    def get_vote_text(self):
        pos_votes = Vote.objects.filter( vote = 'U', idea = self).count()
        notr_votes = Vote.objects.filter( vote = 'N', idea = self ).count()
        neg_votes = Vote.objects.filter( vote = 'D', idea = self ).count()
        return "Olumlu: %s Kararsız: %s Olumsuz: %s" %(pos_votes, notr_votes, neg_votes )


class Status(models.Model):
    name = models.CharField(max_length = 128)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/beyin2/filter/status/%s/" % self.id

class Category(models.Model):
    name = models.CharField(max_length = 128)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/beyin2/filter/category/%s/" % self.id

class Vote(models.Model):
    idea = models.ForeignKey("Idea")
    voter = models.ForeignKey(User, related_name = "voter_user")
    vote = models.CharField(max_length = 1, choices = voteChoices)

    def __unicode__(self):
        return self.vote

class ScreenShot(models.Model):
    idea = models.ForeignKey("Idea")
    image = models.ImageField(upload_to = "beyin2/upload", verbose_name = "Resim")
    is_hidden = models.BooleanField( default = False )

    def save(self):
        if not self.is_hidden:
            super(ScreenShot,self).save()

            old_path = os.path.split(self.image.file.name)[0]
            extension =  os.path.splitext(self.image.file.name)[-1]
            new_name = "%s-%s%s" % (self.idea.title,self.id, extension)
            os.rename(self.image.file.name, old_path+"/"+new_name)

            old_url_head = os.path.split(self.image.url)[0]
            self.image.name = "beyin2/upload/"+new_name
        super(ScreenShot,self).save()

    def __unicode__(self):
        return self.image.file.name


class Favorite(models.Model):
    idea = models.ForeignKey("Idea")
    user = models.ForeignKey( User, related_name = "favorite_user" )

    def __unicode__(self):
        return "%s_%s" %(idea, user)

