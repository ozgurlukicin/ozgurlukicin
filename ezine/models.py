# -*- coding: utf-8 -*-

from django.db import models

class Ezine(models.Model):
    title = models.CharField('Başlık', max_length=128, blank=False)
    description = models.TextField('İçindekiler')
    image = models.FileField('Görsel', upload_to='edergi/images/')
    download_300dpi = models.FileField('300dpi dergi', upload_to='edergi/300dpi/')
    size_300dpi = models.CharField("300dpi dergi boyutu", max_length=8)
    download_96dpi = models.FileField('96dpi dergi', upload_to='edergi/96dpi/')
    size_96dpi = models.CharField("96dpi dergi boyutu", max_length=8)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "E-Dergi"
        verbose_name_plural = "E-Dergiler"
