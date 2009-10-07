#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.template import Context, loader

from oi.st.tags import Tag
from oi.forum.models import Topic
from oi.forum.tools import create_forum_topic

CATEGORIES = (
    ("duvar-kagitlari", "Duvar Kağıtları"),
    ("masaustu-goruntuleri", "Ekran Görüntüleri"),
    ("yazitipleri", "Yazıtipleri"),
)

class WallPaperSize:
    def __init__(self, width, height, screen_type):
        self.width, self.height, self.ratio = width, height, screen_type
    def __str__(self):
        return "%dx%d" % (self.width, self.height)

WALLPAPER_SIZES = (
    #n:normal, w:wide, s:special
    WallPaperSize(2880.0, 1800.0, "w"),
    WallPaperSize(1920.0, 1200.0, "w"),
    WallPaperSize(1920.0, 1080.0, "s"),
    WallPaperSize(1680.0, 1050.0, "w"),
    WallPaperSize(1600.0, 1200.0, "n"),
    WallPaperSize(1440.0,  900.0, "w"),
    WallPaperSize(1280.0, 1024.0, "s"),
    WallPaperSize(1280.0,  800.0, "w"),
    WallPaperSize(1152.0,  864.0, "n"),
    WallPaperSize(1024.0,  768.0, "n"),
    WallPaperSize( 800.0,  600.0, "n"),
)

class License(models.Model):
    name = models.CharField(max_length=32, blank=False, unique=True)
    url = models.URLField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Lisans"
        verbose_name_plural = "Lisanslar"

class ThemeItem(models.Model):
    "A theme item mainly consists of screenshots and files to download"
    title = models.CharField(max_length=100, verbose_name="Başlık", help_text="Buraya, ekleyeceğiniz içeriğin ismini yazın.")
    slug = models.SlugField('SEF Başlık', unique=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Etiketler")
    author = models.ForeignKey(User)
    license = models.ForeignKey(License, verbose_name="Lisans")
    text = models.TextField(blank=False, verbose_name="Tanım", help_text="Ekleyeceğiniz dosyalar hakkındaki açıklamalarınızı bu bölümde belirtebilirsiniz.")
    changelog = models.TextField(blank=True, verbose_name="Değişiklik Listesi", help_text="Eklediğiniz içeriğin değişikliklerini sürüm numarası ve sürümdeki değişikliklerin listesi şeklinde belirtebilirsiniz.")
    version = models.CharField("Sürüm Numarası", default="0.1", max_length=16)
    rating = models.IntegerField(default=50, verbose_name="Puan")
    download_count = models.IntegerField(default=0, verbose_name="İndirilme Sayısı")
    submit = models.DateTimeField(verbose_name="Oluşturulma Tarihi")
    update = models.DateTimeField(verbose_name="Düzenlenme Tarihi")
    comment_enabled = models.BooleanField(default=True,verbose_name="Yoruma Açık", help_text="Diğer üyelerin bu içeriğe yorum yapıp yapamayacağını buradan belirtebilirsiniz.")
    thumbnail = models.ImageField("Küçük Resim", blank=True, upload_to="upload/tema/kucuk/")
    status = models.BooleanField(default=False, verbose_name="Kabul Edilmiş")
    topic = models.ForeignKey(Topic, verbose_name="Forumdaki Konusu")
    origin_url = models.URLField("Özgün Çalışma", blank=True, help_text="Başka bir çalışmayı temel aldıysanız bunun bağlantısını yazın.")

    def __unicode__(self):
        return self.title

    def save(self):
        create_forum_topic(self, "Tema")
        if self.thumbnail:
            #update topic post with the thumbnail
            post = self.topic.post_set.order_by("created")[0]
            post.text = loader.get_template("tema/forum_wallpaper.html").render(Context({"object":self}))
            post.save()

        super(ThemeItem, self).save()

    # we only support wallpaper for now, so return wallpaper url.
    # Later, fix this
    def get_absolute_url(self):
        if Wallpaper.objects.filter(id = self.id).count():
            return "/tema/duvar-kagitlari/%s/" % self.slug
        elif DesktopScreenshot.objects.filter(id = self.id).count():
            return "/tema/masaustu-goruntuleri/%s/" % self.slug

    class Meta:
        verbose_name="Sanat Birimi"
        verbose_name_plural="Sanat Birimleri"

    def get_change_url(self):
        return "/tema/duzenle/%s/" % self.id

    def get_abuse_url(self):
        return "/tema/raporla/%s/" % self.id

    def get_rating_url(self):
        return "/tema/oyla/%s/" % self.id

    def get_rating_step(self):
        return 1.0*self.rating/20

    def get_rating_percent(self):
        return 1.0*self.rating/10

    def update_rating(self):
        #we assume all theme items have 10*50 points
        votes = self.vote_set.all()
        vote_total = 500
        for vote in votes:
            vote_total += vote.rating

        self.rating = vote_total/(self.vote_set.count()+10)
        self.save()

    def get_delete_url(self):
        return "/tema/sil/%d/" % self.id

    class Meta:
        permissions = (
            ("manage_queue", "Can Manage Tema Queue"),
        )

class Font(ThemeItem):
    font = models.FileField("Yazıtipi dosyası", upload_to="upload/tema/yazitipi/", verbose_name="Yazıtipi")
    is_turkish = models.BooleanField("Türkçe karakterleri içeriyor", default=True)

    class Meta:
        verbose_name="Yazıtipi"
        verbose_name_plural="Yazıtipleri"

    def get_absolute_url(self):
        return "/tema/yazitipleri/%s/" % (self.slug)

    def get_redirect_url(self):
        return "/tema/yazitipleri/%s/%s/" % (self.slug, self.id)

    def get_download_url(self):
        return self.font.url


class DesktopScreenshot(ThemeItem):
    image = models.ImageField(upload_to="upload/tema/masaustu-goruntusu/", verbose_name="Masaüstü Görüntüsü")

    class Meta:
        verbose_name="Masaüstü Görüntüsü"
        verbose_name_plural="Masaüstü Görüntüleri"

    def get_absolute_url(self):
        return "/tema/masaustu-goruntuleri/%s/" % (self.slug)

    def get_redirect_url(self):
        return "/tema/masaustu-goruntuleri/%s/%s/" % (self.slug, self.id)

    def get_download_url(self):
        return self.image.url


class Wallpaper(ThemeItem):
    papers = models.ManyToManyField("WallpaperFile", blank=True)

    class Meta:
        verbose_name="Duvar Kağıdı"
        verbose_name_plural="Duvar Kağıtları"

    def get_absolute_url(self):
        return "/tema/duvar-kagitlari/%s/" % (self.slug)

    def get_download_url(self):
        return self.papers.all()[0].image.url

    def create_smaller_wallpapers(self, wallpaper, create_other_ratioes=False):
        "create smaller wallpapers from given one"
        #make smaller sizes
        for size in WALLPAPER_SIZES:
            if size.width < wallpaper.image.width:
                #respect the ratio
                if wallpaper.image.width*1.0/wallpaper.image.height == size.width/size.height:
                    image = Image.open(wallpaper.image.path)
                    image.thumbnail((int(size.width),int(size.height)), Image.ANTIALIAS)
                    newPaper = self.papers.create(title=str(size))
                    file = ContentFile("")
                    newPaper.image.save(wallpaper.image.path, file, save=True)
                    image.save(newPaper.image.path)
                #crop a little if it's 1280x1024
                elif wallpaper.image.width == 1280 and wallpaper.image.height == 1024:
                    image = Image.open(wallpaper.image.path).crop((0, 32, 1280, 992))
                    image.thumbnail((int(size.width),int(size.height)), Image.ANTIALIAS)
                    newPaper = self.papers.create(title=str(size))
                    file = ContentFile("")
                    newPaper.image.save(wallpaper.image.path, file, save=True)
                    image.save(newPaper.image.path)

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
    title = models.CharField("Başlık", max_length=32, blank=True, help_text="Boyuta göre otomatik doldurulmasını istiyorsanız boş bırakabilirsiniz.")
    scalable = models.BooleanField(default=False)
    image = models.ImageField(upload_to="upload/tema/duvar-kagidi/", verbose_name="Duvar Kağıdı")

    def get_absolute_url(self):
        return "/tema/duvar-kagitlari/%s/%s/" % (self.wallpaper_set.all()[0].slug, self.id)

    def get_download_url(self):
        return self.image.url

    def __unicode__(self):
        return self.title or "..." + self.image.name[-24:]

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


class ThemeAbuseReport(models.Model):
    themeitem = models.ForeignKey(ThemeItem, verbose_name='Tema İletisi')
    submitter = models.ForeignKey(User, verbose_name='Raporlayan kullanıcı')
    reason = models.TextField(max_length=512, blank=False, verbose_name="Sebep")

    class Meta:
        verbose_name = 'İleti şikayeti'
        verbose_name_plural = 'İleti şikayetleri'
