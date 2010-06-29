#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


voteChoices = (
            ( 'U', '+1'),
            ( 'D', '-1'),
            ( 'N', ' 0'),
)


class Idea(models.Model):
    title = models.CharField(max_length = 128)
    description = models.TextField()
    dateSubmitted = models.DateTimeField("date submitted",default=datetime.now())
    submitter = models.ForeignKey(User)
    status = models.ForeignKey("Status")
    category = models.ForeignKey("Category")
    
    def __unicode__(self):
	return self.title

class Status(models.Model):
    name = models.CharField(max_length = 128)
    
    def __unicode__(self):
	return self.name


class Category(models.Model):
    name = models.CharField(max_length = 128)
    
    def __unicode__(self):
	return self.name

class Vote(models.Model):
    idea = models.ForeignKey("Idea")
    vote = models.CharField(max_length= 1, choices=voteChoices)
    
    def __unicode__(self):
	return self.vote

class ScreenShot(models.Model):
    idea = models.ForeignKey("Idea")
    image = models.ImageField(upload_to="beyin2/")
    
    def __unicode__(self):
	return self.image.file.name



