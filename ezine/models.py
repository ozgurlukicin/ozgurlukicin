# -*- coding: utf-8 -*-

from django.db import models
from oi.upload.models import Image

import os

class Ezine(models.Model):
    issue = models.PositiveIntegerField("Sayı", primary_key=True, unique=True)
    title = models.CharField('Başlık', max_length=64, help_text="alt satıra düşmesi için arada &lt;br/&gt; kullanın \"Özgürlükİçin e-dergi &lt;br/&gt; Şubat / Mart 2009\" gibi")
    description = models.TextField('İçindekiler')
    image = models.ForeignKey(Image, verbose_name="Dergi Görseli", blank=True, null=True, help_text="Görselin 310x205 boyutlarında olmasına dikkat edin! Yeni görsel eklemek için + düğmesine tıklayın.")
    editor = models.CharField('Editör', max_length=64)
    page_count = models.PositiveIntegerField("Sayfa sayısı")
    download_300dpi = models.CharField('300dpi dergi adresi', max_length=256, help_text="/media/dosya/oi_say11_buyuk.pdf gibi")
    size_300dpi = models.PositiveIntegerField("300dpi dergi boyutu", help_text="bayt cinsinden")
    download_96dpi = models.CharField('96dpi dergi adresi', max_length=256, help_text="/media/dosya/oi_say11_kucuk.pdf gibi")
    size_96dpi = models.PositiveIntegerField("96dpi dergi boyutu", help_text="bayt cinsinden")
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "E-Dergi"
        verbose_name_plural = "E-Dergiler"

class EzineFile(models.Model):
    episode = models.ForeignKey("Ezine", verbose_name="Sayı", unique=True)
    file_size_300dpi = models.FileField(upload_to="dosya", verbose_name="300dpi dergi dosyası")
    file_size_96dpi = models.FileField(upload_to="dosya", verbose_name="96dpi dergi dosyası")

    def save(self):
        super(EzineFile, self).save()
        ezine_files = [(self.file_size_300dpi, "buyuk"), (self.file_size_96dpi, "kucuk")]
        for ezine in ezine_files:
            ezine_file, size = ezine
            path = os.path.split(ezine_file.file.name)[0]
            extension = os.path.splitext(ezine_file.file.name)[-1]
            new_name = "oi_say%s_%s%s" % (str(self.episode.issue), size, extension)
            os.rename(ezine_file.file.name, "%s/%s" % (path, new_name))
            ezine_file.name = "dosya/%s" % new_name
        super(EzineFile, self).save()

    def __unicode__(self):
        return "E-Dergi %d. Sayı" % self.episode.issue

    class Meta:
        verbose_name = "E-Dergi Dosyası"
        verbose_name_plural = "E-Dergi Dosyaları"
