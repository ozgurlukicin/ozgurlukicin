#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re, Image
from os import path, stat, remove
from commands import getoutput

from django.db import models
from django.contrib.auth.models import User

from oi.middleware import threadlocals
from oi.settings import CITY_LIST, MEDIA_ROOT, MEDIA_URL

class Tag(models.Model):
    name = models.CharField('Etiket', maxlength=32, blank=False, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/etiket/%s/" % self.name

    class Admin:
        list_display = ('name', 'id')
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        ordering = ['name']
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"

class Contribute(models.Model):
    name = models.CharField('Tanım', maxlength=64, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'id')
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        verbose_name = "Katkı Adı"
        verbose_name_plural = "Katkı Adları"

class ScreenShot(models.Model):
    desc = models.TextField('Açıklama')
    file = models.ImageField(upload_to='ekran_goruntusu/')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.file

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

    class Admin:
        list_display = ('file', 'desc')
        ordering = ['-id']
        search_fields = ['file', 'desc']

    class Meta:
        verbose_name = "Ekran Görüntüsü"
        verbose_name_plural = "Ekran Görüntüleri"

class Video(models.Model):
    desc = models.CharField('Açıklama', maxlength=64)
    file = models.FileField(upload_to='upload/video/')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.desc

    def get_thumbnail_url(self):
        return "%s%s.png" % (MEDIA_URL, path.splitext(self.file)[0])

    class Admin:
        list_display = ('file', 'desc')
        ordering = ['-id']
        search_fields = ['file', 'desc']

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"

    def convertvideo(self, video):
        filename = path.splitext(self.file)[0]
        sourcefile = "%s%s" % (MEDIA_ROOT, self.file)
        flvfilename = "%s.flv" % filename
        thumbnailfilename = "%s%s.png" % (MEDIA_ROOT, filename)
        targetfile = "%s%s" % (MEDIA_ROOT, flvfilename)
        ffmpeg = "ffmpeg -i %s -acodec mp3 -ar 22050 -ab 32 -f flv -s 320x240 %s" % (sourcefile,  targetfile)
        grabimage = "ffmpeg -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s 236x176 %s " % (sourcefile, thumbnailfilename)
        flvtool = "flvtool2 -U %s" % targetfile

        ffmpegresult = getoutput(ffmpeg)

        s = stat(targetfile)
        fsize = s.st_size
        if (fsize == 0):
            remove(targetfile)

        flvresult = getoutput(flvtool)
        grab = getoutput(grabimage)

        remove(sourcefile)

        return "%s" % flvfilename

    def save(self):
        self.file = self.convertvideo(file)
        super(Video, self).save()

class License(models.Model):
    name = models.CharField(maxlength=16, blank=False, unique=True)
    url = models.URLField()

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('id', 'name')

    class Meta:
        verbose_name = "Lisans"
        verbose_name_plural = "Lisanslar"

class FS(models.Model):
    title = models.CharField('Başlık', maxlength=32, blank=False)
    slug = models.SlugField('SEF Başlık', prepopulate_from=("title",))
    sum = models.TextField('Özet', blank=False)
    text = models.TextField('Metin', blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField('Son Güncelleme', blank=False)
    author = models.CharField('Yazar', maxlength=32)
    status = models.BooleanField('Aktif')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/ia/%s/" % self.slug

    def get_printable_url(self):
        return "/ia/%s/yazdir/" % self.slug

    class Admin:
        fields = (
            ('Genel', {'fields': ('author', 'title','sum','text','videos','tags','update','status',)}),
            ('Diğer', {'fields': ('slug',), 'classes': 'collapse'}),
        )

        list_display = ('title', 'status', 'update')
        list_filter = ['update']
        ordering = ['-update']
        search_fields = ['title', 'text', 'tags']
        js = ("js/admin/sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    class Meta:
        verbose_name = "İlk Adım"
        verbose_name_plural = "İlk Adımlar"

class HowTo(models.Model):
    title = models.CharField('Başlık', maxlength=32, blank=False)
    slug = models.SlugField('SEF Başlık', prepopulate_from=("title",))
    sum = models.TextField('Özet', blank=False)
    text = models.TextField('Metin', blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField('Son Güncelleme', blank=False)
    author = models.CharField('Yazar', maxlength=32)
    status = models.BooleanField('Aktif')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/nasil/%s/" % self.slug

    def get_printable_url(self):
        return "/nasil/%s/yazdir/" % self.slug

    class Admin:
        fields = (
            ('Genel', {'fields': ('author', 'title','sum','text','videos','tags','update','status',)}),
            ('Diğer', {'fields': ('slug',), 'classes': 'collapse'}),
        )

        list_display = ('title', 'status', 'update')
        list_filter = ['update']
        ordering = ['-update']
        search_fields = ['title', 'text', 'tags']
        js = ("js/admin/sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    class Meta:
        verbose_name = "Nasıl"
        verbose_name_plural = "Nasıl Belgeleri"

class Game(models.Model):
    ratings = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'))

    title = models.CharField('Başlık', maxlength=32, blank=False)
    slug = models.SlugField('SEF Başlık', prepopulate_from=("title",))
    sum = models.TextField('Özet', blank=False)
    text = models.TextField('Metin', blank=False)
    license = models.ManyToManyField(License)
    installed_size = models.IntegerField('Kurulu boyut', help_text='Byte cinsinden')
    download_size = models.IntegerField('İndirilecek boyut', help_text='Byte cinsinden')
    url = models.URLField('Sitesi', verify_exists=True, help_text='Başına http:// koymayı unutmayın')
    path = models.CharField('Çalıştırma Yolu', maxlength=128, help_text='Paketin Pardus menüsündeki yeri (örn. Programlar > Yardımcı Programlar > KNazar)')
    gameplay = models.SmallIntegerField('Oynanabilirlik', maxlength=1, choices=ratings)
    graphics = models.SmallIntegerField('Grafik', maxlength=1, choices=ratings)
    sound = models.SmallIntegerField('Ses', maxlength=1, choices=ratings)
    scenario = models.SmallIntegerField('Senaryo', maxlength=1, choices=ratings)
    atmosphere = models.SmallIntegerField('Atmosfer', maxlength=1, choices=ratings)
    learning_time = models.CharField('Öğrenme Süresi', maxlength=128, help_text='1 gün, 3 saat, 5 ay, yıllarca gibi.')
    tags = models.ManyToManyField(Tag, blank=False)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField('Son Güncelleme', blank=False)
    author = models.CharField('Yazar', maxlength=32)
    status = models.BooleanField('Aktif')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/oyun/%s/" % self.slug

    def get_printable_url(self):
        return "/oyun/%s/yazdir/" % self.slug

    class Admin:
        fields = (
            ('Genel', {'fields': ('author', 'title', 'sum', 'text', 'videos', 'tags', 'update', 'status')}),
            ('Oyun bilgileri', {'fields': ('url', 'path', 'learning_time', 'license', 'installed_size', 'download_size')}),
            ('Değerlendirme', {'fields': ('gameplay', 'graphics', 'sound', 'scenario', 'atmosphere')}),
            ('Diğer', {'fields': ('slug',), 'classes': 'collapse'}),
        )
        list_display = ('title', 'status', 'update')
        list_filter = ['update']
        ordering = ['-id']
        search_fields = ['title', 'sum', 'text', 'tags']
        js = ("js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    class Meta:
        verbose_name = "Oyun"
        verbose_name_plural = "Oyunlar"

class News(models.Model):
    title = models.CharField('Başlık', maxlength=32, blank=False)
    slug = models.SlugField('SEF Başlık', prepopulate_from=("title",))
    sum = models.TextField('Özet', blank=False)
    text = models.TextField('Metin', blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    update = models.DateTimeField('Tarih', blank=False)
    author = models.CharField('Yazar', maxlength=32)
    status = models.BooleanField('Aktif')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/haber/%s/" % self.slug

    def get_printable_url(self):
        return "/haber/%s/yazdir/" % self.slug

    class Admin:
        fields = (
            ('Genel', {'fields': ('author', 'title', 'sum', 'text', 'tags', 'update', 'status')}),
            ('Diğer', {'fields': ('slug',), 'classes': 'collapse'}),
        )

        list_display = ('title', 'author', 'update','status')
        list_filter = ['update']
        ordering = ['-update']
        search_fields = ['title', 'author', 'text']
        js = ("js/tinymce/tiny_mce.js", "js/tinymce/textareas.js")

    class Meta:
        verbose_name = "Haber"
        verbose_name_plural = "Haberler"


class Package(models.Model):
    ratings = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'))

    title = models.CharField('Başlık', maxlength=32, blank=False, help_text='Paket ismi')
    slug = models.SlugField('SEF Başlık', prepopulate_from=("title",))
    sum = models.TextField('Özet', blank=False)
    text = models.TextField('Açıklama', blank=False)
    license = models.ManyToManyField(License)
    installed_size = models.IntegerField('Kurulu boyut', help_text='Byte cinsinden')
    download_size = models.IntegerField('İndirilecek boyut', help_text='Byte cinsinden')
    url = models.URLField('Sitesi', verify_exists=True, help_text='Başına http:// koymayı unutmayın')
    point = models.SmallIntegerField('Editör Notu', maxlength=1, choices=ratings)
    path = models.CharField('Çalıştırma Yolu', maxlength=128, help_text='Paketin Pardus menüsündeki yeri (örn. Programlar > Yardımcı Programlar > KNazar)')
    ss = models.ManyToManyField(ScreenShot)
    tags = models.ManyToManyField(Tag)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField('Son Güncelleme', blank=False)
    author = models.CharField('Yazar', maxlength=32)
    status = models.BooleanField('Aktif')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/paket/%s/" % self.slug

    def get_printable_url(self):
        return "/paket/%s/yazdir/" % self.slug

    class Admin:
        fields = (
            ('Genel', {'fields': ('author', 'title','sum','text', 'license','installed_size','download_size','url','point','path','ss','tags','videos','update','status')}),
            ('Diğer', {'fields': ('slug',), 'classes': 'collapse'}),
        )
        list_display = ('title', 'status', 'update')
        list_filter = ['license']
        ordering = ['-id']
        search_fields = ['title', 'sum', 'text']
        js = ("js/admin/package_sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    class Meta:
        verbose_name = "Paket"
        verbose_name_plural = "Paketler"

class PardusVersion(models.Model):
    number = models.CharField('Sürüm numarası', maxlength = 16, blank = False, unique = True)
    codename = models.CharField('Kod adı', maxlength = 64, unique = True)
    install_md5sum = models.CharField('Kurulan md5 özeti', maxlength = 32, blank = False, unique = True)
    install_sha1sum = models.CharField('Kurulan sha1 özeti', maxlength = 40, blank = False, unique = True)
    live_md5sum = models.CharField('Çalışan md5 özeti', maxlength = 32, blank = False, unique = True)
    live_sha1sum = models.CharField('Çalışan sha1 özeti', maxlength = 40, blank = False, unique = True)
    releasenote = models.TextField('Sürüm notu', blank = False)
    install_torrent = models.CharField('Kurulan Torrent', maxlength = 128)
    live_torrent = models.CharField('Çalışan Torrent', maxlength = 128)
    status = models.BooleanField('Aktif')

    def __str__(self):
        return "Pardus %s" % self.number

    def get_absolute_url(self):
        return "/indir/%s/" % self.number

    class Admin:
        list_display = ('number', 'codename', 'status')
        ordering = ['-number']
        search_fields = ['codename']
        js = ("js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    class Meta:
        verbose_name = "Pardus Sürümü"
        verbose_name_plural = "Pardus Sürümleri"

class PardusMirror(models.Model):
    cdtype = (('1','Kurulan'),('2','Çalışan'))

    name = models.CharField('Sunucu adı', maxlength = 64, blank = False, unique = True)
    url = models.CharField('Adres', maxlength = 128)
    type = models.SmallIntegerField('CD Tipi', maxlength=1, choices=cdtype)
    status = models.BooleanField('Aktif')

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'url', 'status')
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        verbose_name = "Pardus Yansısı"
        verbose_name_plural = "Pardus Yansıları"
