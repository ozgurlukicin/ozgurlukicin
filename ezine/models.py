# -*- coding: utf-8 -*-

from django.db import models
from oi.upload.models import Image
from django.utils.translation import ugettext as _

class Ezine(models.Model):
    issue = models.PositiveIntegerField(_("Issue"), primary_key=True, unique=True)
    title = models.CharField(_("Title"), max_length=64, help_text=_("use &lt;br/&gt; to break line like \"Spread Pardus E-zine &lt;br/&gt; March 2009\""))
    description = models.TextField(_("Contents"))
    image = models.ForeignKey(Image, verbose_name=_("E-zine Image"), blank=True, null=True, help_text="Note that image should be 310x205 in size! Press + to add new image.")
    editor = models.CharField(_('Editor'), max_length=64)
    page_count = models.PositiveIntegerField(_("Page count"))
    download_300dpi = models.CharField(_("300dpi e-zine address"), max_length=256, help_text=_("like /media/dosya/sp_i11_big.pdf"))
    size_300dpi = models.PositiveIntegerField(_("300dpi e-zine size"), help_text=_("in bytes"))
    download_96dpi = models.CharField(_("96dpi e-zine address"), max_length=256, help_text=_("like /media/dosya/sp_i11_sml.pdf"))
    size_96dpi = models.PositiveIntegerField(_("96dpi e-zine size"), help_text=_("in bytes"))
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("E-Zine")
        verbose_name_plural = _("E-Zines")
