# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.template import Context, loader
from django.core.mail import EmailMessage
from django.db.models.signals import post_save,post_delete

from oi.st.tags import Tag
from oi.forum.models import Topic
from oi.forum.tools import create_forum_topic
from oi.settings import WEB_URL, DEFAULT_FROM_EMAIL
from oi.tema.settings import TEMA_ADMIN_MAIL

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

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    order = models.PositiveIntegerField(verbose_name='Sıralama')
    count = models.IntegerField(blank=True, null=True, default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class WallpaperCategory(Category):
    class Meta:
        verbose_name = u"Duvar Kağıdı Kategorisi"
        verbose_name_plural = u"Duvar Kağıdı Kategorileri"

class OpenOfficeTemplateCategory(Category):
    class Meta:
        verbose_name = u"Open Office Şablon Kategorisi"
        verbose_name_plural = u"Open Office Şablon Kategorileri"

class OpenOfficeExtensionCategory(Category):
    class Meta:
        verbose_name = u"Open Office Eklenti Kategorisi"
        verbose_name_plural = u"Open Office Eklenti Kategorileri"

class ThemeItem(models.Model):
    "A theme item mainly consists of screenshots and files to download"
    title = models.CharField(max_length=100, verbose_name="Başlık", help_text="Buraya, ekleyeceğiniz içeriğin ismini yazın.")
    slug = models.SlugField('SEF Başlık', unique=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Etiketler")
    author = models.ForeignKey(User)
    license = models.ForeignKey(License, verbose_name="Lisans")
    text = models.TextField(blank=False, verbose_name="Tanım", help_text="Ekleyeceğiniz dosyalar hakkındaki açıklamalarınızı bu bölümde belirtebilirsiniz.")
    changelog = models.TextField(blank=True, verbose_name="Değişiklik Listesi", help_text="Eklediğiniz içeriğin değişikliklerini sürüm numarası ve sürümdeki değişikliklerin listesi şeklinde belirtebilirsiniz.")
    version = models.CharField("Sürüm Numarası", default="", max_length=16, blank=True, help_text="0.1 gibi")
    rating = models.IntegerField(default=50, verbose_name="Puan")
    download_count = models.IntegerField(default=0, verbose_name="İndirilme Sayısı")
    submit = models.DateTimeField(verbose_name="Oluşturulma Tarihi")
    update = models.DateTimeField(verbose_name="Düzenlenme Tarihi")
    comment_enabled = models.BooleanField(default=True,verbose_name="Yoruma Açık", help_text="Diğer üyelerin bu içeriğe yorum yapıp yapamayacağını buradan belirtebilirsiniz.")
    thumbnail = models.ImageField("Küçük Resim", blank=True, upload_to="upload/tema/kucuk/")
    status = models.BooleanField(default=False, verbose_name="Kabul Edilmiş")
    deny_reason = models.TextField(blank=True, verbose_name="Reddetme Nedeni",
            help_text="Kabul edilmediyse sebebini yazın (ekleyen kişiye gönderilecek e-posta metni)")
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
        if self.status:
            #send mail to author? (this should only send once when accepted)
            pass
        if not self.status and self.deny_reason:
            message = loader.get_template("tema/mail/rejected.html").render(Context({"themeitem":self,"WEB_URL":WEB_URL}))
            mail = EmailMessage(
                "Özgürlükiçin Tema - Reddedilen İçerik",
                message,
                "Özgürlükiçin Tema <%s>" % TEMA_ADMIN_MAIL,
                [self.author.email]
            )
            mail.send(fail_silently=True)

        new_content = False
        if self.id == None:
            new_content = True

        super(ThemeItem, self).save()
        if new_content:
            #send mail to admins
            message = loader.get_template("tema/mail/new_content.html").render(Context({"themeitem":self,"WEB_URL":WEB_URL}))
            mail = EmailMessage(
                "Özgürlükiçin Tema - Yeni İçerik",
                message,
                "Özgürlükiçin <%s>" % DEFAULT_FROM_EMAIL,
                [TEMA_ADMIN_MAIL]
            )
            mail.send(fail_silently=True)

    def get_absolute_url(self):
        if Wallpaper.objects.filter(id = self.id).count():
            return "/tema/duvar-kagitlari/detay/%s/" % self.slug
        elif DesktopScreenshot.objects.filter(id = self.id).count():
            return "/tema/masaustu-goruntuleri/detay/%s/" % self.slug
        elif Font.objects.filter(id = self.id).count():
            return "/tema/yazitipleri/detay/%s/" % self.slug
        elif OpenOfficeTemplate.objects.filter(id = self.id).count():
            return "/tema/open-office-sablon/detay/%s/" % self.slug
        elif OpenOfficeExtension.objects.filter(id = self.id).count():
            return "/tema/open-office-eklenti/detay/%s/" % self.slug
        elif IconSet.objects.filter(id = self.id).count():
            return "/tema/simge-seti/detay/%s/" % self.slug
        elif PackageScreenshot.objects.filter(id= self.id).count():
            return "/tema/paket-goruntuleri/detay/%s/" % self.slug



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

    def is_new(self):
        now = datetime.datetime.now()
        one_week = 7 * 24 * 60
        if self.submit - now < one_week:
            return "new"
        elif self.update - now < one_week:
            return "updated"
        else:
            return "not-new"

    class Meta:
        permissions = (
            ("manage_queue", "Can Manage Tema Queue"),
        )

class IconSet(ThemeItem):
    file = models.FileField("Simge Seti Dosyası", upload_to="upload/tema/iconset/%Y/%m/%d")
    screenshot = models.ImageField("Ekran görüntüsü", help_text="Simge setinizin nasıl göründüğüne dair bir ekran görüntünüzü burada paylaşın",upload_to="upload/tema/openoffice/%Y/%m/%d",blank=False,null=True)

    class Meta:
        verbose_name = "Simge Seti"
        verbose_name_plural = "Simge Setleri"

    def get_absolute_url(self):
        return "/tema/simge-seti/detay/%s/" % self.slug

    def get_redirect_url(self):
        return "/tema/simge-seti/detay/%s/%s/" % (self.slug, self.id)

    def get_download_url(self):
        return self.file.url

class OpenOfficeApplication(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class OpenOfficeVersion(models.Model):
    version = models.CharField(max_length=50)
    version_number = models.PositiveIntegerField()

    def __unicode__(self):
        return self.version


class OpenOfficeTheme(ThemeItem):
    file = models.FileField("OpenOffice dosyası", upload_to="upload/tema/openoffice/%Y/%m/%d")
    screenshot = models.ImageField("Ekran görüntüsü", help_text="Şablonunuzun nasıl göründüğüne dair bir ekran görüntünüzü burada paylaşın", upload_to="upload/tema/openoffice/%Y/%m/%d",blank=True,null=True)

    class Meta:
        verbose_name = "Open Office özelleştirmesi"
        verbose_name_plural = "Open Office özelleştirmeleri"

    def get_absolute_url(self):
        if OpenOfficeTemplate.objects.filter(id = self.id).count():
            return "/tema/open-office-sablon/detay/%s/" % self.slug
        elif OpenOfficeExtension.objects.filter(id = self.id).count():
            return "/tema/open-office-eklenti/detay/%s/" % self.slug

class OpenOfficeTemplate(OpenOfficeTheme):
    category = models.ForeignKey("OpenOfficeTemplateCategory",verbose_name="Kategori")

    class Meta:
        verbose_name = u"Open Office Şablonu"
        verbose_name_plural = u"Open Office Şablonları"

    def get_absolute_url(self):
        return "/tema/open-office-sablon/detay/%s/" % (self.slug)

    def get_redirect_url(self):
        return "/tema/open-office-sablon/detay/%s/%s/" % (self.slug, self.id)

    def get_download_url(self):
        return self.file.url

class OpenOfficeExtension(OpenOfficeTheme):
    category = models.ForeignKey("OpenOfficeExtensionCategory") 

    class Meta:
        verbose_name = u"Open Office Eklentisi"
        verbose_name_plural = u"Open Office Eklentileri"

    def get_absolute_url(self):
        return "/tema/open-office-eklenti/detay/%s/" % (self.slug)

    def get_redirect_url(self):
        return "/tema/open-office-eklenti/detay/%s/%s" % (self.slug, self.id)

    def get_download_url(self):
        return self.file.url

class Font(ThemeItem):
    font = models.FileField("Yazıtipi dosyası", upload_to="upload/tema/yazitipi/")
    is_turkish = models.BooleanField("Türkçe karakterleri içeriyor", default=True)

    class Meta:
        verbose_name="Yazıtipi"
        verbose_name_plural="Yazıtipleri"

    def get_absolute_url(self):
        return "/tema/yazitipleri/detay/%s/" % (self.slug)

    def get_redirect_url(self):
        return "/tema/yazitipleri/detay/%s/%s/" % (self.slug, self.id)

    def get_download_url(self):
        return self.font.url


class DesktopScreenshot(ThemeItem):
    image = models.ImageField(upload_to="upload/tema/masaustu-goruntusu/", verbose_name="Masaüstü Görüntüsü")

    class Meta:
        verbose_name="Masaüstü Görüntüsü"
        verbose_name_plural="Masaüstü Görüntüleri"

    def get_absolute_url(self):
        return "/tema/masaustu-goruntuleri/detay/%s/" % (self.slug)

    def get_redirect_url(self):
        return "/tema/masaustu-goruntuleri/detay/%s/%s/" % (self.slug, self.id)

    def get_download_url(self):
        return self.image.url



class Wallpaper(ThemeItem):
    papers = models.ManyToManyField("WallpaperFile", blank=True)
    category = models.ForeignKey("WallpaperCategory", null=True,verbose_name="Kategori")

    class Meta:
        verbose_name="Duvar Kağıdı"
        verbose_name_plural="Duvar Kağıtları"

    def get_absolute_url(self):
        return "/tema/duvar-kagitlari/detay/%s/" % (self.slug)

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


class PackageScreenshot(ThemeItem):
    image = models.ImageField(upload_to="upload/tema/paket-goruntusu/buyuk", verbose_name="Paket Görüntüsü")
    s_image = models.ImageField(upload_to="upload/tema/paket-goruntusu/kucuk", verbose_name="Küçük Resim")

    class Meta:
        verbose_name = "Paket Görüntüsü"
        verbose_name_plural = "Paket Görüntüleri"

    def get_absolute_url(self):
        return "/tema/paket-goruntuleri/detay/%s/" % self.slug

    def get_redirect_url(self):
        return "/tema/paket-goruntuleri/detay/%s/%s/" % (self.slug, self.id)

    def get_download_url(self):
        return self.image.url


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
        return "/tema/duvar-kagitlari/detay/%s/%s/" % (self.wallpaper_set.all()[0].slug, self.id)

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

def category_counter_callback(sender, **kwargs):
    instance = kwargs["instance"]
    Model = instance.__class__
    Category = Model.category.field.rel.to
    for category in Category.objects.all():
        category.count = Model.objects.filter(category=category,status=True).count()
        category.save()

for Model in [Wallpaper,OpenOfficeTemplate, OpenOfficeExtension]:
    post_save.connect(category_counter_callback, sender=Model)
    post_delete.connect(category_counter_callback, sender=Model)
