#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from oi.st.tags import Tag

CATEGORIES = (
    ("duvar-kagitlari", "Duvar Kağıtları"),
    ("ekran-goruntuleri", "Ekran Görüntüleri"),
)

WALLPAPER_SIZES_H = (
    (800, "800"),
    (1024, "1024"),
    (1152, "1152"),
    (1280, "1280"),
    (1440, "1440"),
    (1600, "1600"),
    (1920, "1920"),
)
WALLPAPER_SIZES_V = (
    (600, "600"),
    (768, "768"),
    (864, "864"),
    (900, "900"),
    (1024, "1024"),
    (1050, "1050"),
    (1080, "1080"),
    (1200, "1200"),
)
class WallPaperSize:
    def __init__(self, width, height, screen_type):
        self.width, self.height, self.ratio = width, height, screen_type
    def __str__(self):
        return "%dx%d" % (self.width, self.height)

WALLPAPER_SIZES = (
    WallPaperSize( 800,  600, "n"),
    WallPaperSize(1024,  768, "n"),
    WallPaperSize(1152,  864, "n"),
    WallPaperSize(1280,  800, "w"),
    WallPaperSize(1280, 1024, "n"),
    WallPaperSize(1440,  900, "w"),
    WallPaperSize(1600, 1200, "n"),
    WallPaperSize(1680, 1050, "w"),
    WallPaperSize(1920, 1200, "w"),
)

class License(models.Model):
    name = models.CharField(max_length=16, blank=False, unique=True)
    url = models.URLField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Lisans"
        verbose_name_plural = "Lisanslar"

class ThemeItem(models.Model):
    "A theme item mainly consists of screenshots and files to download"
    name = models.CharField(max_length=100, unique=True, verbose_name="Başlık", help_text="Buraya, ekleyeceğiniz içeriğin ismini yazın.")
    category = models.CharField("Kategori", max_length=24, choices=CATEGORIES)
    tags = models.ManyToManyField(Tag, verbose_name="Etiketler")
    author = models.ForeignKey(User)
    license = models.ForeignKey(License, verbose_name="Lisans")
    description = models.TextField(blank=False, verbose_name="Tanım", help_text="Ekleyeceğiniz dosyalar hakkındaki açıklamalarınızı bu bölümde belirtebilirsiniz.")
    changelog = models.TextField(blank=True, verbose_name="Değişiklik Listesi", help_text="Eklediğiniz içeriğin değişikliklerini sürüm numarası ve sürümdeki değişikliklerin listesi şeklinde belirtebilirsiniz.")
    rating = models.IntegerField(default=50, verbose_name="Puan")
    download_count = models.IntegerField(default=0, verbose_name="İndirilme Sayısı")
    submit_date = models.DateTimeField(verbose_name="Oluşturulma Tarihi")
    edit_date = models.DateTimeField(verbose_name="Düzenlenme Tarihi")
    comment_enabled = models.BooleanField(default=True,verbose_name="Yoruma Açık", help_text="Diğer üyelerin bu içeriğe yorum yapıp yapamayacağını buradan belirtebilirsiniz.")
    thumbnail = models.ImageField("Küçük Resim", blank=True, upload_to="upload/tema/kucuk/")
    #TODO: change this to False before we're on air
    approved = models.BooleanField(default=True, verbose_name="Kabul Edilmiş")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name="Sanat Birimi"
        verbose_name_plural="Sanat Birimleri"

    def get_absolute_url(self):
        return "/tema/%s/%s/" % (self.category, self.id)

    def get_change_url(self):
        return "/tema/duzenle/%s/" % self.id

class Wallpaper(ThemeItem):
    scalable = models.BooleanField(default=False)
    papers = models.ManyToManyField("WallpaperFile")

    class Meta:
        verbose_name="Duvar Kağıdı"
        verbose_name_plural="Duvar Kağıtları"

    def create_smaller_wallpapers(self, wallpaper, create_other_ratioes=True):
        "create smaller wallpapers from given one"
        #calculate sizes to create
        for size in WALLPAPER_SIZES:
            if size.width < wallpaper.image.width:
                image = Image.open(wallpaper.image.path)
                image.thumbnail((size.width,size.height), Image.ANTIALIAS)
                newPaper = self.papers.create(title=str(size))
                #FIXME: Those don't work, dunno why
                #newPaper.image.save(wallpaper.image.path, image.getdata(), save=True)
                #newPaper.image.save(wallpaper.image.path, image.tostring(), save=True)

class File(models.Model):
    "File for download"
    title = models.CharField(max_length=100, verbose_name="Başlık", help_text="Buraya, dosyanın kullanıcılara görünecek adını yazın.")
    file = models.FileField(upload_to="upload/tema/dosya/")

    class Meta:
        verbose_name = "Dosya"
        verbose_name_plural = "Dosyalar"

    def __unicode__(self):
        return self.file

class ScreenShot(models.Model):
    "Screenshot of a theme item"
    image = models.ImageField(upload_to="upload/tema/goruntu/", verbose_name="Görüntü")

    def __unicode__(self):
        return self.image.name

    class Meta:
        verbose_name = "Ekran Görüntüsü"
        verbose_name_plural = "Ekran Görüntüleri"

class WallpaperFile(models.Model):
    "A wallpaper file"
    title = models.CharField("Başlık", max_length=32, blank=True)
    image = models.ImageField(upload_to="upload/tema/goruntu/", verbose_name="Görüntü")

    def __unicode__(self):
        return self.title or self.image.name

    class Meta:
        verbose_name = "Duvar Kağıdı Dosyası"
        verbose_name_plural = "Duvar Kağıdı Dosyaları"

class Vote(models.Model):
    "Vote of a user"

    theme_item = models.ForeignKey(ThemeItem)
    user = models.ForeignKey(User)
    rating = models.IntegerField(default=50, verbose_name="Puan")

    class Meta:
        verbose_name = "Oy"
        verbose_name_plural = "Oylar"
