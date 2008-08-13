#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from django.db import models
from django.contrib.auth.models import User
from oi.st.models import Tag


class StatusCategory(models.Model):
    name = models.CharField("İsim", max_length=128)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name = "Durum Kategorisi"
        verbose_name_plural = "Durum Kategorileri"

class Status(models.Model):
    category = models.ForeignKey(StatusCategory, verbose_name = "Durum Kategori")
    name = models.CharField("İsim", max_length = 128)


    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name = "Durum"
        verbose_name_plural = "Durum"


class Category(models.Model):
    name = models.CharField("İsim", max_length=150)
    slug = models.SlugField("SEF isim", prepopulate_from=('name',))

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

class RelatedCategory(models.Model):
    name = models.CharField("İsim", max_length=150)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name = "İlgili Kategorisi"
        verbose_name_plural = "İlgili Kategorisi"

class Related(models.Model):
    category = models.ForeignKey(RelatedCategory, verbose_name = "Kategori")
    name = models.CharField("İsim", max_length=150)
#    slug = models.SlugField(prepopulate_from('name',))

    def __unicode__(self):
        return self.name

    class Admin:
        pass

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
    related_to = models.ForeignKey(Related, null=True, verbose_name="Şununla ilgili")
    tags = models.ManyToManyField(Tag, verbose_name="Etiketler")
    vote_count = models.IntegerField("Oy Sayısı", default=0)
    duplicate = models.ForeignKey("self", blank=True, null=True, verbose_name="Fikir Tekrarı")
    is_duplicate = models.BooleanField("Fikir Tekrarı", default=False)
    forum_url = models.URLField("İlgili forum bağlantısı", help_text="Varsa ilgili Özgürlük İçin Forumundaki konu adresini yazın.", blank=True)
    bug_numbers = models.CharField("Hata numaraları", help_text="Varsa ilgili hata numaralarını virgülle ayırarak giriniz.", max_length=64, blank=True)
    file = models.FileField(upload_to="upload/ideas/dosya/", blank=True)
    is_hidden = models.BooleanField("Gizli", default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/yenifikir/ayrinti/%s" % self.id

    class Admin:
        list_display = ('title', 'submitter', 'submitted_date', 'category', 'related_to', 'is_hidden', 'is_duplicate', 'duplicate')
        list_filter = ('status', 'is_hidden', 'is_duplicate',  'category', 'related_to')

    class Meta:
        verbose_name = "Yeni Fikir"
        verbose_name_plural = "Yeni Fikirler"

class Comment(models.Model):
    idea = models.ForeignKey(Idea, verbose_name="İlgili fikir")
    author = models.ForeignKey(User, verbose_name="Yazan",related_name="comments_author")
    text = models.TextField("Yorum")
    submited = models.DateTimeField("Tarih", auto_now_add=True)
    is_hidden = models.BooleanField("Gizli", default=False)
    ip = models.IPAddressField("IP Adresi",blank=True, null=True)

    def __unicode__(self):
        return self.text

    class Admin:
        pass

    class Meta:
        verbose_name="Yorum"
        verbose_name_plural ="Yorumlar"

class Vote(models.Model):
    idea = models.ForeignKey(Idea, verbose_name="Oy Verilen Fikir", related_name="vote_idea", blank=False, null=False)
    user = models.ForeignKey(User, verbose_name="Oy Veren", related_name="vote_author", blank=False, null=False)
    vote = models.BooleanField("Verilen Oy", blank=False)

    class Admin:
        pass

    class Meta:
        verbose_name = "Verilen Oy"
        verbose_name = "Verilan Oylar"

class Favorite(models.Model):
    user = models.ForeignKey(User, verbose_name = "Favorileyen", related_name="fav_author", blank=False)
    idea = models.ForeignKey(Idea, verbose_name = "Favori Fikirler", related_name="fav_idea", blank=False)

    def __unicode__(self):
        return self.idea

    class Admin:
        pass

    class Meta:
        verbose_name = "Favori"
        verbose_name = "Favoriler"
