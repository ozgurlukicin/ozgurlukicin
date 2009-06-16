#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User
from oi.st.models import License

class ParentCategory(models.Model):
    "Each theme item belongs to a ParentCategory and a SubCategory"

    name = models.CharField(max_length=100, verbose_name="Kategori adı", unique=True)
    slug = models.SlugField(verbose_name="SEF Başlık", unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/tema/listele/%s/tumu/tarih/" % (self.slug)
    class Meta:
        verbose_name="Kategori"
        verbose_name_plural="Kategoriler"


class SubCategory(models.Model):
    "Each theme item belongs to a ParentCategory and a SubCategory"

    parent = models.ForeignKey(ParentCategory)
    name = models.CharField(max_length=100, verbose_name="Kategori adı")
    slug = models.SlugField(verbose_name="SEF Başlık", unique=True)

    def __unicode__(self):
        return u"%s > %s" % (self.parent.name, self.name)

    def get_absolute_url(self):
        return "/tema/listele/%s/%s/tarih/" % (self.parent.slug, self.slug)

    class Meta:
        verbose_name="Alt Kategori"
        verbose_name_plural="Alt Kategoriler"


class ThemeItem(models.Model):
    "A theme item mainly consists of screenshots and files to download"

    name = models.CharField(max_length=100, unique=True, verbose_name="Başlık", help_text="Buraya, ekleyeceğiniz içeriğin ismini yazın.")
    parentcategory = models.ForeignKey(ParentCategory, verbose_name="Üst Kategori")
    category = models.ForeignKey(SubCategory, verbose_name="Kategori")
    author = models.ForeignKey(User)
    license = models.ForeignKey(License, verbose_name="Lisans")
    description = models.TextField(blank=False, verbose_name="Tanım", help_text="Ekleyeceğiniz dosyalar hakkındaki açıklamalarınızı bu bölümde belirtebilirsiniz.")
    changelog = models.TextField(blank=True, verbose_name="Değişiklik Listesi", help_text="Eklediğiniz içeriğin değişikliklerini sürüm numarası ve sürümdeki değişikliklerin listesi şeklinde belirtebilirsiniz.")
    rating = models.IntegerField(default=50, verbose_name="Puan")
    download_count = models.IntegerField(default=0, verbose_name="İndirilme Sayısı")
    submit_date = models.DateTimeField(verbose_name="Oluşturulma Tarihi")
    edit_date = models.DateTimeField(verbose_name="Düzenlenme Tarihi")
    comment_enabled = models.BooleanField(default=True,verbose_name="Yoruma Açık", help_text="Diğer üyelerin bu içeriğe yorum yapıp yapamayacağını buradan belirtebilirsiniz.")
    #TODO: change this to False before we're on air
    approved = models.BooleanField(default=True, verbose_name="Kabul Edilmiş")

    class Meta:
        verbose_name="Sanat Birimi"
        verbose_name_plural="Sanat Birimleri"

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name="Sanat Birimi"
        verbose_name_plural="Sanat Birimleri"

    def get_absolute_url(self):
        return "/tema/goster/%s/%s/%s/" % (self.parentcategory.slug, self.category.slug, self.id)

    def get_change_url(self):
        return "/tema/duzenle/%s/%s/%s/" % (self.parentcategory.slug, self.category.slug, self.id)


class File(models.Model):
    "File for download"

    theme_item = models.ForeignKey(ThemeItem)
    title = models.CharField(max_length=100, verbose_name="Başlık", help_text="Buraya, dosyanın kullanıcılara görünecek adını yazın.")
    file = models.FileField(upload_to="upload/tema/dosya/")

    class Meta:
        verbose_name = "Dosya"
        verbose_name_plural = "Dosyalar"

    def __unicode__(self):
        return self.file

class ScreenShot(models.Model):
    "Screenshot of a theme item"

    theme_item = models.ForeignKey(ThemeItem)
    image = models.ImageField(upload_to="upload/tema/goruntu/", verbose_name="Görüntü")
    thumbnail = models.ImageField(upload_to="upload/tema/goruntu/kucuk/", verbose_name="Küçük Resim")

    def __unicode__(self):
        return self.image

    class Meta:
        verbose_name = "Ekran Görüntüsü"
        verbose_name_plural = "Ekran Görüntüleri"

class Vote(models.Model):
    "Vote of a user"

    theme_item = models.ForeignKey(ThemeItem)
    user = models.ForeignKey(User)
    rating = models.IntegerField(default=50, verbose_name="Puan")

    class Meta:
        verbose_name = "Oy"
        verbose_name_plural = "Oylar"
