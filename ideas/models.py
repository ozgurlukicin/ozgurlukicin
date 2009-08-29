#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from django.db import models
from django.contrib.auth.models import User
from oi.st.tags import Tag
from oi.forum.models import Topic


class StatusCategory(models.Model):
    name = models.CharField("İsim", max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Durum Kategorisi"
        verbose_name_plural = "Durum Kategorileri"

class Status(models.Model):
    category = models.ForeignKey(StatusCategory, verbose_name = "Durum Kategori")
    name = models.CharField("İsim", max_length = 128)
    is_invalid = models.BooleanField("Geçersiz", default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Durum"
        verbose_name_plural = "Durum"


class Category(models.Model):
    name = models.CharField("İsim", max_length=150)
    slug = models.SlugField("SEF isim")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def get_absolute_url(self):
        return "/yenifikir/listele/kategori/%s/" % self.slug

class RelatedCategory(models.Model):
    name = models.CharField("İsim", max_length=150)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "İlgili Kategorisi"
        verbose_name_plural = "İlgili Kategorisi"

class Related(models.Model):
    category = models.ForeignKey(RelatedCategory, verbose_name = "Kategori")
    name = models.CharField("İsim", max_length=150)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Fikir şununla ilgili"
        verbose_name_plural = "Fikir şununla ilgili"


class Idea(models.Model):
    title = models.CharField("Başlık", help_text="Fikir başlığı", max_length=100)
    submitted_date = models.DateTimeField("Tarih", auto_now_add=True)
    submitter = models.ForeignKey(User, verbose_name="Gönderen")
    description = models.TextField("Açıklama", help_text="Fikrinizi açıklayan bir yazı yazın.")
    status = models.ForeignKey(Status,verbose_name="Durum")
    category = models.ForeignKey(Category, null=True, verbose_name="Kategori")
    related_to = models.ForeignKey(Related, blank=True, null=True, verbose_name="Şu paketle ilgili", help_text="Bu alanı boş bırakabilirsiniz.")
    tags = models.ManyToManyField(Tag, verbose_name="Etiketler")
    vote_count = models.IntegerField("Oy Sayısı", default=0)
    duplicate = models.ForeignKey("self", blank=True, null=True, verbose_name="Fikir Tekrarı")
    is_duplicate = models.BooleanField("Fikir Tekrarı", default=False)
    forum_url = models.URLField("İlgili forum bağlantısı", help_text="Varsa ilgili Özgürlük İçin Forumundaki konu adresini yazın.", blank=True)
    bug_numbers = models.CharField("Hata numaraları", help_text="Varsa ilgili hata numaralarını virgülle ayırarak giriniz.", max_length=63, blank=True)
    file = models.FileField(upload_to="upload/ideas/dosya/", blank=True, verbose_name='Dosya')
    is_hidden = models.BooleanField("Gizli", default=False)
    topic = models.ForeignKey(Topic, verbose_name="Fikrin Forumdaki Konusu")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/yenifikir/ayrinti/%s/" % self.id

    class Meta:
        verbose_name = "Yeni Fikir"
        verbose_name_plural = "Yeni Fikirler"

class Vote(models.Model):
    idea = models.ForeignKey(Idea, verbose_name="Oy Verilen Fikir", related_name="vote_idea", blank=False, null=False)
    user = models.ForeignKey(User, verbose_name="Oy Veren", related_name="vote_author", blank=False, null=False)
    vote = models.IntegerField("Verilen Oy", blank=False)

    def __unicode__(self):
        return self.idea

    class Meta:
        unique_together = ("idea", "user")
        verbose_name = "Verilen Oy"
        verbose_name_plural = "Verilen Oylar"

class Favorite(models.Model):
    user = models.ForeignKey(User, verbose_name = "Favorileyen", related_name="fav_author", blank=False)
    idea = models.ForeignKey(Idea, verbose_name = "Favori Fikirler", related_name="fav_idea", blank=False)

    def __unicode__(self):
        return self.idea

    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoriler"
