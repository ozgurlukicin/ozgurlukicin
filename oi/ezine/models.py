# -*- coding: utf-8 -*-

from django.db import models
from oi.upload.models import Image

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
