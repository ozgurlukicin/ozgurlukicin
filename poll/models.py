#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Uğur Çetin
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

class PollVote(models.Model):
    poll = models.ForeignKey("Poll", verbose_name="Anket")
    option = models.ForeignKey("PollOption", verbose_name="Seçenek")
    voter = models.ForeignKey(User)
    voter_ip = models.IPAddressField(blank=True, verbose_name="IP Adresi")

    def __unicode__(self):
        return self.option.__unicode__()

    class Admin:
        list_display = ("option", "voter", "voter_ip")
        ordering = ["option"]
        search_fields = ["voter_ip"]

    class Meta:
        verbose_name = "Anket Oyu"
        verbose_name_plural = "Anket Oyları"


class PollOption(models.Model):
    poll = models.ForeignKey("Poll", verbose_name="Anket")
    text = models.CharField("Yazı", max_length=128)
    vote_count = models.IntegerField(default=0, verbose_name="Oy sayısı")

    def __unicode__(self):
        if len(self.text) > 32:
            return "%s..." % self.question[:30]
        else:
            return self.text

    class Admin:
        list_display = ("poll", "text", "vote_count")
        ordering = ["poll"]
        search_fields = ["text"]

    class Meta:
        verbose_name = "Anket Seçeneği"
        verbose_name_plural = "Anket Seçenekleri"


class Poll(models.Model):
    question = models.CharField("Soru", max_length=128, help_text="Buraya anketin sorusunu yazın.")
    allow_changing_vote = models.BooleanField("Oy Değiştirmek İzinli", default=False, blank=True, help_text="Kullanılan oyların sonradan değiştirilebilmesini istiyorsanız bunu işaretleyin.")
    allow_multiple_choices = models.BooleanField("Çok Seçmeli Oylama", default=False, blank=True, help_text="Bir kişinin birden fazla seçenekte oy kullanabilmesini isiyorsanız bunu seçin. Uyarı: Bu ayarı sonradan değiştiremezsiniz.")
    date_limit = models.BooleanField("Süreli", help_text="Oylamada süre sınırı olmasını istiyorsanız bunu işaretleyin.")
    end_date = models.DateTimeField("Bitiş Tarihi", blank=True, null=True, help_text="Oylamanın ne zaman biteceğini belirleyin. 30/8/2008 gibi.")

    def __unicode__(self):
        if len(self.question) > 32:
            return "%s..." % self.question[:30]
        else:
            return self.question

    class Admin:
        list_display = ("question", "allow_changing_vote", "date_limit", "end_date")
        search_fields = ["question"]

    class Meta:
        verbose_name = "Anket"
        verbose_name_plural = "Anketler"
