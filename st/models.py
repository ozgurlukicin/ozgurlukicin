#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import Image
from django.db import models
from django.contrib.auth.models import User
from oi.middleware import threadlocals

class Tag(models.Model):
    name = models.CharField('Etiket', maxlength = 32, blank=False, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/tag/%s/" % self.name

    class Admin:
        list_display = ('name', 'id')
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"

class UserProfile(models.Model):
    homepage = models.URLField()
    user = models.ForeignKey(User, unique=True)

    class Admin:
        list_display = ('user', 'homepage',)
        ordering = ['-user']
        search_fields = ['user']

        fields = (
                ('Kullanıcı', {
                    'fields': ('user',)
                    }),
                ('Üyelik Bilgileri', {
                    'fields': ('homepage',)
                    }),
                  )

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"

class ScreenShot(models.Model):
    desc = models.TextField('Açıklama')
    file = models.ImageField(upload_to='ekran_goruntusu/')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.file

    def get_thumbnail_url(file, size='230x230'):
        thumb = 'thumb_' + file
        thumb_filename = os.path.join(settings.MEDIA_ROOT, thumb)
        thumb_url = os.path.join(settings.MEDIA_URL, thumb)

        if not os.path.exists(thumb_filename):
            filename = os.path.join(settings.MEDIA_ROOT, file)
            image = Image.open(filename)
            image.thumbnail([230, 230])
            image.save(thumb_filename, image.format)

        return thumb_url

    class Admin:
        list_display = ('file', 'desc')
        list_filter = ['tags']
        ordering = ['-id']
        search_fields = ['file', 'desc']

    class Meta:
        verbose_name = "Ekran Görüntüsü"
        verbose_name_plural = "Ekran Görüntüleri"

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
    sef_title = models.CharField('SEF Başlık', maxlength=32, blank=False, unique=True)
    text = models.TextField('Metin', blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    update = models.DateTimeField('Son Güncelleme', blank=False)

    def __str__(self):
        return self.sef_title

    def get_absolute_url(self):
        return "/ia/%s/" % self.sef_title

    def get_printable_url(self):
        return "/ia/%s/yazdir/" % self.sef_title

    class Admin:
        fields = (
            ('Genel', {'fields': ('title','text','tags','update',)}),
            ('Diğer', {'fields': ('sef_title',), 'classes': 'collapse'}),
        )

        list_display = ('title', 'text', 'update')
        list_filter = ['update']
        ordering = ['-update']
        search_fields = ['title', 'text', 'tags']
        js = ("js/admin/sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    class Meta:
        verbose_name = "İlk Adım"
        verbose_name_plural = "İlk Adımlar"

class Game(models.Model):
    title = models.CharField('Başlık', maxlength=32, blank=False)
    sef_title = models.CharField('SEF Başlık', maxlength=32, blank=False, unique=True)
    text = models.TextField('Metin', blank=False)
    ss = models.ManyToManyField(ScreenShot)
    tags = models.ManyToManyField(Tag, blank=False)
    update = models.DateTimeField('Tarih', blank=False)

    def __str__(self):
        return self.sef_title

    def get_absolute_url(self):
        return "/oyun/%s/" % self.sef_title

    def get_printable_url(self):
        return "/oyun/%s/yazdir/" % self.sef_title

    class Admin:
        fields = (
            ('Genel', {'fields': ('title','text', 'ss', 'tags','update',)}),
            ('Diğer', {'fields': ('sef_title',), 'classes': 'collapse'}),
        )
        list_display = ('title', 'text', 'update')
        list_filter = ['tags', 'update']
        ordering = ['-id']
        search_fields = ['title', 'text', 'tags']
        js = ("js/admin/sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    class Meta:
        verbose_name = "Oyun"
        verbose_name_plural = "Oyunlar"

class News(models.Model):
    title = models.CharField('Başlık', maxlength=32, blank=False)
    sef_title = models.CharField('SEF Başlık', maxlength=32, blank=False, unique=True)
    sum = models.TextField('Özet', blank=False)
    text = models.TextField('Metin', blank=False)
    author = models.ForeignKey(User, blank=True, editable=False)
    tags = models.ManyToManyField(Tag, blank=False)
    date = models.DateTimeField('Tarih', blank=False)

    def __str__(self):
        return self.sef_title

    def get_absolute_url(self):
        return "/haber/%s/" % self.sef_title

    def get_printable_url(self):
        return "/haber/%s/yazdir/" % self.sef_title

    def save(self):
        self.author = threadlocals.get_current_user()
        super(News, self).save()

    class Admin:
        fields = (
            ('Genel', {'fields': ('title','sum','text','tags','date',)}),
            ('Diğer', {'fields': ('sef_title',), 'classes': 'collapse'}),
        )

        list_display = ('title', 'author', 'date')
        list_filter = ['author', 'date']
        ordering = ['-date']
        search_fields = ['title', 'text']
        js = ("js/admin/sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js", "js/getElementsBySelector.js", "js/filebrowser/AddFileBrowser.js",)

    class Meta:
        verbose_name = "Haber"
        verbose_name_plural = "Haberler"


class Package(models.Model):
    ratings = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'))

    name = models.CharField('İsim', maxlength=32, help_text='Paket ismi')
    sum = models.TextField('Özet')
    desc = models.TextField('Açıklama')
    license = models.ManyToManyField(License)
    installed_size = models.IntegerField('Kurulu boyut', help_text='Byte cinsinden')
    download_size = models.IntegerField('İndirilecek boyut', help_text='Byte cinsinden')
    url = models.URLField('Sitesi', verify_exists=True, help_text='Başına http:// koymayı unutmayın')
    point = models.SmallIntegerField('Editör Notu', maxlength=1, choices=ratings)
    path = models.CharField('Çalıştırma Yolu', maxlength=128, help_text='Paketin Pardus menüsündeki yeri (örn. Programlar > Yardımcı Programlar > KNazar)')
    ss = models.ManyToManyField(ScreenShot)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/paket/%s/" % self.name

    def get_printable_url(self):
        return "/paket/%s/yazdir/" % self.name

    class Admin:
        list_display = ('name', 'sum')
        list_filter = ['license', 'tags']
        ordering = ['-id']
        search_fields = ['name', 'sum', 'desc']
        js = ("js/admin/package_sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    class Meta:
        verbose_name = "Paket"
        verbose_name_plural = "Paketler"
