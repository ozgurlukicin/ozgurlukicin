#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007, 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re, Image
from os import path, stat, remove
import subprocess

from django.db import models
from django.contrib.auth.models import User

from oi.middleware import threadlocals
from oi.settings import CITY_LIST, MEDIA_ROOT, MEDIA_URL
from oi.forum.models import Topic
from oi.forum.tools import create_forum_topic

# the signal stuff
from django.db.models import signals
from oi.st.tags import Tag
from oi.st.signals import remove_video_thumbnail_on_delete
from oi.upload.models import Image as Img

FFMPEG_COMMAND = "ffmpeg"

class Wiki(models.Model):
    name = models.CharField('Madde adı', max_length=128, blank=False, unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "http://tr.pardus-wiki.org/%s" % self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Wiki sayfası"
        verbose_name_plural = "Wiki sayfaları"

class Contribute(models.Model):
    name = models.CharField('Tanım', max_length=64, blank=False, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Katkı Adı"
        verbose_name_plural = "Katkı Adları"

class OtherFile(models.Model):
    desc = models.TextField('Açıklama')
    file = models.FileField(upload_to='dosya/')
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return unicode(self.file)

    class Meta:
        verbose_name = "Dosya"
        verbose_name_plural = "Dosyalar"

class ScreenShot(models.Model):
    desc = models.TextField('Açıklama')
    file = models.ImageField(upload_to='ekran_goruntusu/')
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return unicode(self.file)

    def get_thumbnail_url(file, size='230x230'):
        thumb = 'thumb_' + file
        thumb_filename = path.join(MEDIA_ROOT, thumb)
        thumb_url = path.join(MEDIA_URL, thumb)

        if not path.exists(thumb_filename):
            filename = path.join(MEDIA_ROOT, file)
            image = Image.open(filename)

            s = size.split("x")
            image.thumbnail([s[0], s[1]])

            image.save(thumb_filename, image.format)

        return thumb_url

    class Meta:
        verbose_name = "Ekran Görüntüsü"
        verbose_name_plural = "Ekran Görüntüleri"

class Video(models.Model):
    desc = models.CharField('Açıklama', max_length=64)
    file = models.FileField(upload_to='upload/video/')
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.desc

    def get_thumbnail_url(self):
        return "%s%s.png" % (MEDIA_URL, path.splitext(self.file)[0])

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"

    def convertvideo(self, video):
        filename = path.splitext(self.file)[0]
        sourcefile = "%s%s" % (MEDIA_ROOT, self.file)
        flvfilename = "%s.flv" % filename
        thumbnailfilename = "%s%s.png" % (MEDIA_ROOT, filename)
        targetfile = "%s%s" % (MEDIA_ROOT, flvfilename)
        ffmpeg = (FFMPEG_COMMAND, "-i", sourcefile, "-ar", "22050", "-ab", "32768", "-f", "flv", "-s", "320x240", targetfile)
        grabimage = (FFMPEG_COMMAND, "-y", "-i", sourcefile, "-vframes", "1", "-ss", "00:00:02", "-an", "-vcodec", "png", "-f", "rawvideo", "-s", "220x176", thumbnailfilename)

        if not sourcefile == targetfile:
            ffmpegresult = subprocess.call(ffmpeg)
            grab = subprocess.call(grabimage)
            remove(sourcefile)

        s = stat(targetfile)
        fsize = s.st_size
        if (fsize == 0):
            remove(targetfile)

        return "%s" % flvfilename

    def save(self):
        self.file = self.convertvideo(file)
        super(Video, self).save()

    def get_video_name(self):
        return path.splitext(self.file)[0].split('/')[2]

signals.pre_delete.connect(remove_video_thumbnail_on_delete, sender=Video)

class License(models.Model):
    name = models.CharField(max_length=16, blank=False, unique=True)
    url = models.URLField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Lisans"
        verbose_name_plural = "Lisanslar"

class FS(models.Model):
    title = models.CharField('Başlık', max_length=32, blank=False)
    slug = models.SlugField('SEF Başlık')
    image = models.ForeignKey(Img, verbose_name="Görsel", blank=True, null=True)
    sum = models.TextField('Özet', blank=False)
    text = models.TextField('Metin', blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField('Son Güncelleme', blank=False)
    author = models.CharField('Yazar', max_length=32)
    order = models.PositiveIntegerField(unique=True, verbose_name='Sıralama')
    status = models.BooleanField('Aktif')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/ia/%s/" % self.slug

    def get_printable_url(self):
        return "/ia/%s/yazdir/" % self.slug

    class Meta:
        verbose_name = "İlk Adım"
        verbose_name_plural = "İlk Adımlar"

class HowTo(models.Model):
    title = models.CharField('Başlık', max_length=32, blank=False)
    slug = models.SlugField('SEF Başlık')
    sum = models.TextField('Özet', blank=False)
    image = models.ForeignKey(Img, verbose_name="Görsel", blank=True, null=True)
    text = models.TextField('Metin', blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    wiki = models.ManyToManyField(Wiki, blank=True)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField('Son Güncelleme', blank=False)
    author = models.CharField('Yazar', max_length=32)
    status = models.BooleanField('Aktif')
    topic = models.ForeignKey(Topic, verbose_name="Forumdaki Konusu")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/nasil/%s/" % self.slug

    def get_printable_url(self):
        return "/nasil/%s/yazdir/" % self.slug

    def save(self):
        create_forum_topic(self, "Nasıl")
        super(HowTo, self).save()

    class Meta:
        verbose_name = "Nasıl"
        verbose_name_plural = "Nasıl Belgeleri"

class Game(models.Model):
    ratings = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'))

    title = models.CharField('Başlık', max_length=32, blank=False)
    slug = models.SlugField('SEF Başlık')
    image = models.ForeignKey(Img, verbose_name="Görsel", blank=True, null=True)
    sum = models.TextField('Özet', blank=False)
    text = models.TextField('Metin', blank=False)
    license = models.ManyToManyField(License)
    installed_size = models.IntegerField('Kurulu boyut', help_text='Byte cinsinden')
    download_size = models.IntegerField('İndirilecek boyut', help_text='Byte cinsinden')
    url = models.URLField('Sitesi', verify_exists=True, help_text='Başına http:// koymayı unutmayın')
    path = models.CharField('Çalıştırma Yolu', max_length=128, help_text='Paketin Pardus menüsündeki yeri (örn. Programlar > Yardımcı Programlar > KNazar)')
    gameplay = models.SmallIntegerField('Oynanabilirlik', max_length=1, choices=ratings)
    graphics = models.SmallIntegerField('Grafik', max_length=1, choices=ratings)
    sound = models.SmallIntegerField('Ses', max_length=1, choices=ratings)
    scenario = models.SmallIntegerField('Senaryo', max_length=1, choices=ratings)
    atmosphere = models.SmallIntegerField('Atmosfer', max_length=1, choices=ratings)
    learning_time = models.CharField('Öğrenme Süresi', max_length=128, help_text='1 gün, 3 saat, 5 ay, yıllarca gibi.')
    tags = models.ManyToManyField(Tag, blank=False)
    wiki = models.ManyToManyField(Wiki, blank=True)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField('Son Güncelleme', blank=False)
    author = models.CharField('Yazar', max_length=32)
    status = models.BooleanField('Aktif')
    topic = models.ForeignKey(Topic, verbose_name="Forumdaki Konusu")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/oyun/%s/" % self.slug

    def get_printable_url(self):
        return "/oyun/%s/yazdir/" % self.slug

    def save(self):
        create_forum_topic(self, "Oyunlar")
        super(Game, self).save()

    class Meta:
        verbose_name = "Oyun"
        verbose_name_plural = "Oyunlar"

class News(models.Model):
    title = models.CharField('Başlık', max_length=32, blank=False)
    slug = models.SlugField('SEF Başlık', help_text="Haberin bağlantısını oluşturacak başlık (haber başlığıyla aynı olmalı fakat sadece küçük harf ve - içermelidir)")
    image = models.ForeignKey(Img, verbose_name="Açılış Görseli", blank=True, null=True, help_text="Görselin 310x205 boyutlarında olmasına dikkat edin! Yeni görsel eklemek için + düğmesine tıklayın.")
    sum = models.TextField('Özet', blank=False, help_text="Açılış görseli haber özetine otomatik eklenecektir.")
    text = models.TextField('Metin', blank=False)
    tags = models.ManyToManyField(Tag, verbose_name="Etiketler", blank=False)
    update = models.DateTimeField('Tarih', blank=False)
    author = models.CharField('Yazar', max_length=32)
    status = models.BooleanField('Aktif')
    topic = models.ForeignKey(Topic, verbose_name="Forumdaki Konusu")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/haber/%s/" % self.slug

    def get_printable_url(self):
        return "/haber/%s/yazdir/" % self.slug

    def save(self):
        create_forum_topic(self, "Haberler")
        super(News, self).save()

    class Meta:
        verbose_name = "Haber"
        verbose_name_plural = "Haberler"

class Package(models.Model):
    ratings = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'))

    title = models.CharField('Başlık', max_length=32, blank=False, help_text='Paket ismi')
    slug = models.SlugField('SEF Başlık')
    image = models.ForeignKey(Img, verbose_name="Görsel", blank=True, null=True)
    sum = models.TextField('Özet', blank=False)
    text = models.TextField('Açıklama', blank=False)
    license = models.ManyToManyField(License)
    installed_size = models.IntegerField('Kurulu boyut', help_text='Byte cinsinden')
    download_size = models.IntegerField('İndirilecek boyut', help_text='Byte cinsinden')
    url = models.URLField('Sitesi', verify_exists=True, help_text='Başına http:// koymayı unutmayın')
    point = models.SmallIntegerField('Editör Notu', max_length=1, choices=ratings)
    path = models.CharField('Çalıştırma Yolu', max_length=128, help_text='Paketin Pardus menüsündeki yeri (örn. Programlar > Yardımcı Programlar > KNazar)')
    ss = models.ManyToManyField(ScreenShot)
    tags = models.ManyToManyField(Tag)
    wiki = models.ManyToManyField(Wiki, blank=True)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField('Son Güncelleme', blank=False)
    author = models.CharField('Yazar', max_length=32)
    status = models.BooleanField('Aktif')
    topic = models.ForeignKey(Topic, verbose_name="Forumdaki Konusu")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/paket/%s/" % self.slug

    def get_printable_url(self):
        return "/paket/%s/yazdir/" % self.slug

    def save(self):
        create_forum_topic(self, "Paketler")
        super(Package, self).save()

    class Meta:
        verbose_name = "Paket"
        verbose_name_plural = "Paketler"

class PardusVersion(models.Model):
    number = models.CharField('Sürüm numarası', max_length = 16, blank = False, unique = True)
    codename = models.CharField('Kod adı', max_length = 64, unique = True)
    install_md5sum = models.CharField('Kurulan md5 özeti', max_length = 32, blank = False, unique = True)
    install_sha1sum = models.CharField('Kurulan sha1 özeti', max_length = 40, blank = False, unique = True)
    live_md5sum = models.CharField('Çalışan md5 özeti', max_length = 32, blank = False, unique = True)
    live_sha1sum = models.CharField('Çalışan sha1 özeti', max_length = 40, blank = False, unique = True)
    releasenote = models.TextField('Sürüm notu', blank = False)
    install_torrent = models.CharField('Kurulan Torrent', max_length = 128)
    live_torrent = models.CharField('Çalışan Torrent', max_length = 128)
    status = models.BooleanField('Aktif')

    def __unicode__(self):
        return "Pardus %s" % self.number

    def get_absolute_url(self):
        return "/indir/%s/" % self.number

    class Meta:
        verbose_name = "Pardus Sürümü"
        verbose_name_plural = "Pardus Sürümleri"

class PardusMirror(models.Model):
    cdtype = (('1','Kurulan'),('2','Çalışan'))

    name = models.CharField('Sunucu adı', max_length = 64, blank = False)
    url = models.CharField('Adres', max_length = 128)
    type = models.SmallIntegerField('CD Tipi', max_length=1, choices=cdtype)
    order = models.PositiveIntegerField(verbose_name='Sıralama')
    status = models.BooleanField('Aktif')

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('type', 'order'),('type', 'name'),)
        verbose_name = "Pardus Yansısı"
        verbose_name_plural = "Pardus Yansıları"
