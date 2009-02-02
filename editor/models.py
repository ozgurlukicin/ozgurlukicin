#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

from oi.st.models import News

class ContributedNews(models.Model):
    news = models.ForeignKey(News)
    contributor = models.ForeignKey(User)

    def __unicode__(self):
        return self.news.title
