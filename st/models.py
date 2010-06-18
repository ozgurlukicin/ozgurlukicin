#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007, 2008 TÜBİTAK UEKAE
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
from oi.upload.models import Logo

from django.utils.translation import ugettext as _

FFMPEG_COMMAND = "ffmpeg"
ratings = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10'))

class Wiki(models.Model):
    name = models.CharField(_("Article Name"), max_length=128, blank=False, unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "http://tr.pardus-wiki.org/%s" % self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("Wiki page")
        verbose_name_plural = _("Wiki pages")

class Contribute(models.Model):
    name = models.CharField(_("Description"), max_length=64, blank=False, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Contribution Name")
        verbose_name_plural = _("Contribution Names")

class OtherFile(models.Model):
    desc = models.TextField(_("Description"))
    file = models.FileField(upload_to='dosya/')
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return unicode(self.file)

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

class ScreenShot(models.Model):
    desc = models.TextField(_("Description"))
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
        verbose_name = _("Screenshot")
        verbose_name_plural = _("Screenshots")

class Video(models.Model):
    desc = models.CharField(_("Description"), max_length=64)
    file = models.FileField(upload_to='upload/video/')
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.desc

    def get_thumbnail_url(self):
        return "%s%s.png" % (MEDIA_URL, path.splitext(self.file)[0])

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

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
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")

class FS(models.Model):
    title = models.CharField(_("Title"), max_length=32, blank=False)
    slug = models.SlugField(_("SEF Title"))
    image = models.ForeignKey(Img, verbose_name=_("Image"), blank=True, null=True)
    sum = models.TextField(_("Summary"), blank=False)
    text = models.TextField(_("Text"), blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField(_("Last Update"), blank=False)
    author = models.CharField(_("Author"), max_length=32)
    order = models.PositiveIntegerField(unique=True, verbose_name=_("Ordering"))
    status = models.BooleanField(_("Active"))

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/ia/%s/" % self.slug

    def get_printable_url(self):
        return "/ia/%s/yazdir/" % self.slug

    class Meta:
        verbose_name = _("First Step")
        verbose_name_plural = _("First Steps")

class Workshop(models.Model):
    title = models.CharField(_("Title"), max_length=32, blank=False)
    slug = models.SlugField(_("SEF Title"))
    logo = models.ForeignKey(Logo, blank=True, null=True, help_text=_("must be 114x114 in size"))
    sum = models.TextField(_("Summary"), blank=False)
    image = models.ForeignKey(Img, verbose_name=_("Image"), blank=True, null=True)
    text = models.TextField(_("Text"), blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    update = models.DateTimeField(_("Last Update"), blank=False)
    author = models.CharField(_("Author"), max_length=32)
    status = models.BooleanField(_("Active"))
    topic = models.ForeignKey(Topic)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/atolye/%s/" % self.slug

    def get_printable_url(self):
        return "/atolye/%s/yazdir/" % self.slug

    def save(self):
        create_forum_topic(self, "Atölye")
        super(Workshop, self).save()

    class Meta:
        verbose_name = _("Workshop Article")
        verbose_name_plural = _("Workshop Articles")

class HowTo(models.Model):
    title = models.CharField(_("Title"), max_length=32, blank=False)
    slug = models.SlugField(_("SEF Title"))
    logo = models.ForeignKey(Logo, blank=True, null=True, help_text=_("must be 114x114 in size"))
    sum = models.TextField(_("Summary"), blank=False)
    image = models.ForeignKey(Img, verbose_name=_("Image"), blank=True, null=True)
    text = models.TextField(_("Text"), blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    wiki = models.ManyToManyField(Wiki, blank=True)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField(_("Last Update"), blank=False)
    author = models.CharField(_("Author"), max_length=32)
    status = models.BooleanField(_("Active"))
    topic = models.ForeignKey(Topic)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/nasil/%s/" % self.slug

    def get_printable_url(self):
        return "/nasil/%s/yazdir/" % self.slug

    def save(self):
        create_forum_topic(self, "Nasıl Belgeleri")
        super(HowTo, self).save()

    class Meta:
        verbose_name = _("Howto")
        verbose_name_plural = _("Howto Articles")

class Game(models.Model):
    title = models.CharField(_("Title"), max_length=32, blank=False)
    slug = models.SlugField(_("SEF Title"))
    image = models.ForeignKey(Img, verbose_name=_("Image"), blank=True, null=True)
    sum = models.TextField(_("Summary"), blank=False)
    text = models.TextField(_("Text"), blank=False)
    license = models.ManyToManyField(License)
    installed_size = models.IntegerField(_("Installed size"), help_text=_("in MB"))
    download_size = models.IntegerField(_("Download size"), help_text=_("in MB"))
    url = models.URLField(_("Web Site"), verify_exists=True, help_text=_("Add http:// in front"))
    path = models.CharField(_("Location in Menu"), max_length=128, help_text=_("like Programs > Accesories > KNazar)"))
    gameplay = models.SmallIntegerField(_("Playability"), max_length=1, choices=ratings)
    graphics = models.SmallIntegerField(_("Graphics"), max_length=1, choices=ratings)
    sound = models.SmallIntegerField(_("Sound"), max_length=1, choices=ratings)
    scenario = models.SmallIntegerField(_("Scenario"), max_length=1, choices=ratings)
    atmosphere = models.SmallIntegerField(_("Atmosphere"), max_length=1, choices=ratings)
    learning_time = models.CharField(_("Learning Time"), max_length=128, help_text=_('like 1 day, 3 hours, 5 months, years.'))
    tags = models.ManyToManyField(Tag, blank=False)
    wiki = models.ManyToManyField(Wiki, blank=True)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField(_("Last Update"), blank=False)
    author = models.CharField(_("Author"), max_length=32)
    status = models.BooleanField(_("Active"))
    topic = models.ForeignKey(Topic)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/oyun/%s/" % self.slug

    def get_printable_url(self):
        return "/oyun/%s/yazdir/" % self.slug

    def save(self):
        create_forum_topic(self, "Oyun İncelemeleri")
        super(Game, self).save()

    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")

class News(models.Model):
    title = models.CharField(_("Title"), max_length=32, blank=False)
    slug = models.SlugField(_("SEF Title"), help_text=_("Should be the same as title but only consist of small letters and -"), unique=True)
    image = models.ForeignKey(Img, verbose_name=_("Headline Image"), blank=True, null=True, help_text=_("Image should be 310x205 in size! Press + to upload a new image."))
    sum = models.TextField(_("Summary"), blank=False, help_text=_("Headline image will be added to summary automaticly."))
    text = models.TextField(_("Text"), blank=False)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), blank=False)
    update = models.DateTimeField(_("Update Date"), blank=False)
    author = models.CharField(_("Author"), max_length=32)
    status = models.BooleanField(_("Active"))
    topic = models.ForeignKey(Topic)

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
        verbose_name = _("News")
        verbose_name_plural = _("News")

class Package(models.Model):
    title = models.CharField(_("Title"), max_length=32, blank=False, help_text='Paket ismi')
    slug = models.SlugField(_("SEF Title"))
    image = models.ForeignKey(Img, verbose_name=_("Image"), blank=True, null=True)
    sum = models.TextField(_("Summary"), blank=False)
    text = models.TextField(_("Description"), blank=False)
    license = models.ManyToManyField(License)
    installed_size = models.IntegerField(_("Installed Size"), help_text=_("in MB"))
    download_size = models.IntegerField(_("Download Size"), help_text=_("in MB"))
    url = models.URLField(_("Web Site"), verify_exists=True, help_text=_("Add http:// in front"))
    point = models.SmallIntegerField(_("Editor's Rating"), max_length=1, choices=ratings)
    path = models.CharField(_("Location in Menu"), max_length=128, help_text=_("like Programs > Accesories > KNazar)"))
    ss = models.ManyToManyField(ScreenShot)
    tags = models.ManyToManyField(Tag)
    wiki = models.ManyToManyField(Wiki, blank=True)
    videos = models.ManyToManyField(Video, blank=True)
    update = models.DateTimeField(_("Last Update"), blank=False)
    author = models.CharField(_("Author"), max_length=32)
    status = models.BooleanField(_("Active"))
    topic = models.ForeignKey(Topic)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/paket/%s/" % self.slug

    def get_printable_url(self):
        return "/paket/%s/yazdir/" % self.slug

    def save(self):
        create_forum_topic(self, "Paket Tanıtımları")
        super(Package, self).save()

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")

class PardusVersion(models.Model):
    number = models.CharField(_("Version number"), max_length = 16, blank = False, unique = True)
    codename = models.CharField(_("Code Name"), max_length = 64, unique = True)
    install_md5sum = models.CharField(_("MD5 sum of Install"), max_length = 32, blank = False, unique = True)
    install_sha1sum = models.CharField(_("SHA1 sum of Install"), max_length = 40, blank = False, unique = True)
    live_md5sum = models.CharField(_("MD5 sum of Live"), max_length = 32, blank = False, unique = True)
    live_sha1sum = models.CharField(_("SHA1 sum of Live"), max_length = 40, blank = False, unique = True)
    releasenote = models.TextField(_("Release Notes"), blank = False)
    install_torrent = models.CharField(_("Install Torrent"), max_length = 128)
    live_torrent = models.CharField(_("Live Torrent"), max_length = 128)
    status = models.BooleanField(_("Active"))

    def __unicode__(self):
        return "Pardus %s" % self.number

    def get_absolute_url(self):
        return "/indir/%s/" % self.number

    class Meta:
        verbose_name = _("Pardus Version")
        verbose_name_plural = _("Pardus Versions")

class PardusMirror(models.Model):
    cdtype = ((1,_("Install")),(2,_("Live")))

    name = models.CharField(_("Server name"), max_length = 64, blank = False)
    url = models.CharField(_("Address"), max_length = 128)
    type = models.SmallIntegerField(_("CD Type"), max_length=1, choices=cdtype)
    order = models.PositiveIntegerField(verbose_name=_("Ordering"))
    status = models.BooleanField(_("Active"))

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('type', 'order'),('type', 'name'),)
        verbose_name = _("Pardus Mirror")
        verbose_name_plural = _("Pardus Mirrors")
