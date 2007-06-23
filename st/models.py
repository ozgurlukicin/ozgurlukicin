#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re, Image

from django.db import models
from django.contrib.auth.models import User
from django import newforms as forms

from oi.middleware import threadlocals
from oi.settings import CITY_LIST

#==========
# DB Models
#==========

class Tag(models.Model):
    name = models.CharField('Etiket', maxlength = 32, blank=False, unique=True)

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
    """ Contributes select field in user register page """
    name = models.CharField('Ad', maxlength=32, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'id')
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        verbose_name = "Katkı Adı"
        verbose_name_plural = "Katkı Adları"

class IgnoredUsername(models.Model):
    """ Ignored user name model to prevent the site from slang :) This is controlled in register page"""
    name = models.CharField("Kullanıcı adı", maxlength=30)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name',)
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        verbose_name = "Yasaklanan Kullanıcı Adı"
        verbose_name_plural = "Yasaklanan Kullanıcı Adları"

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='Kullanıcı')
    homepage = models.URLField('Ana Sayfa', blank=True)
    im = models.EmailField('Bağlantı Adresi', blank=True, help_text='Jabber, Gtalk, Msn vs.')
    city = models.CharField('Şehir', choices=CITY_LIST, maxlength=40)
    show_email = models.BooleanField('E-posta Göster')
    register_date = models.DateField('Kayıt Tarihi', auto_now_add=True) # it adds a date when this class is first created
    contributes = models.ManyToManyField(Contribute, blank=True, verbose_name='Katkılar')
    contributes_summary = models.TextField('Katkı Açıklaması', blank=True)
    activation_key = models.CharField(maxlength=40)
    key_expires = models.DateTimeField()

    def __str__(self):
        return self.user.username

    class Admin:
        fields = (
            ('Kullanıcı', {'fields': ('user',)}),
            ('Üyelik Bilgileri', {'fields': ('homepage','im', 'city', 'contributes', 'contributes_summary','register_date', 'show_email',)}),
            ('Diğer', {'fields': ('activation_key', 'key_expires'), 'classes': 'collapse',}),
        )

        list_display = ('user', 'city',)
        ordering = ['-user']
        search_fields = ['user']

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
    status = models.BooleanField('Aktif')

    def __str__(self):
        return self.sef_title

    def get_absolute_url(self):
        return "/ia/%s/" % self.sef_title

    def get_printable_url(self):
        return "/ia/%s/yazdir/" % self.sef_title

    class Admin:
        fields = (
            ('Genel', {'fields': ('title','text','tags','update','status',)}),
            ('Diğer', {'fields': ('sef_title',), 'classes': 'collapse'}),
        )

        list_display = ('title', 'update')
        list_filter = ['update']
        ordering = ['-update']
        search_fields = ['title', 'text', 'tags']
        js = ("js/admin/sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    class Meta:
        verbose_name = "İlk Adım"
        verbose_name_plural = "İlk Adımlar"

class Game(models.Model):
    ratings = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'))

    title = models.CharField('Başlık', maxlength=32, blank=False)
    sef_title = models.CharField('SEF Başlık', maxlength=32, blank=False, unique=True)
    sum = models.TextField('Özet', blank=False)
    text = models.TextField('Metin', blank=False)
    icon = models.ImageField(upload_to='oyun/')
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
    update = models.DateTimeField('Son Güncelleme', blank=False)
    author = models.ForeignKey(User, blank=True, editable=False)
    status = models.BooleanField('Aktif')

    def __str__(self):
        return self.sef_title

    def get_absolute_url(self):
        return "/oyun/%s/" % self.sef_title

    def get_printable_url(self):
        return "/oyun/%s/yazdir/" % self.sef_title

    class Admin:
        fields = (
            ('Genel', {'fields': ('title', 'sum', 'text', 'tags', 'update', 'status')}),
            ('Oyun bilgileri', {'fields': ('icon', 'url', 'path', 'learning_time', 'license', 'installed_size', 'download_size')}),
            ('Değerlendirme', {'fields': ('gameplay', 'graphics', 'sound', 'scenario', 'atmosphere')}),
            ('Diğer', {'fields': ('sef_title',), 'classes': 'collapse'}),
        )
        list_display = ('title', 'sum', 'update')
        list_filter = ['update']
        ordering = ['-id']
        search_fields = ['title', 'sum', 'text', 'tags']
        js = ("js/admin/sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    def save(self):
        self.author = threadlocals.get_current_user()
        super(Game, self).save()

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
    status = models.BooleanField('Aktif')

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
            ('Genel', {'fields': ('title','sum','text','tags','date','status')}),
            ('Diğer', {'fields': ('sef_title',), 'classes': 'collapse'}),
        )

        list_display = ('title', 'author', 'date')
        list_filter = ['date']
        ordering = ['-date']
        search_fields = ['title', 'author', 'text']
        js = ("js/admin/sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js", "js/getElementsBySelector.js", "js/filebrowser/AddFileBrowser.js",)

    class Meta:
        verbose_name = "Haber"
        verbose_name_plural = "Haberler"


class Package(models.Model):
    ratings = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'))

    name = models.CharField('İsim', maxlength=32, help_text='Paket ismi')
    sum = models.TextField('Özet', blank=False)
    desc = models.TextField('Açıklama', blank=False)
    license = models.ManyToManyField(License)
    installed_size = models.IntegerField('Kurulu boyut', help_text='Byte cinsinden')
    download_size = models.IntegerField('İndirilecek boyut', help_text='Byte cinsinden')
    url = models.URLField('Sitesi', verify_exists=True, help_text='Başına http:// koymayı unutmayın')
    point = models.SmallIntegerField('Editör Notu', maxlength=1, choices=ratings)
    path = models.CharField('Çalıştırma Yolu', maxlength=128, help_text='Paketin Pardus menüsündeki yeri (örn. Programlar > Yardımcı Programlar > KNazar)')
    ss = models.ManyToManyField(ScreenShot)
    tags = models.ManyToManyField(Tag)
    update = models.DateTimeField('Son Güncelleme', blank=False)
    status = models.BooleanField('Aktif')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/paket/%s/" % self.name

    def get_printable_url(self):
        return "/paket/%s/yazdir/" % self.name

    class Admin:
        list_display = ('name', 'sum')
        list_filter = ['license']
        ordering = ['-id']
        search_fields = ['name', 'sum', 'desc']
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
        list_display = ('number', 'codename')
        ordering = ['-number']
        search_fields = ['codename']
        js = ("js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    class Meta:
        verbose_name = "Pardus Sürümü"
        verbose_name_plural = "Pardus Sürümleri"

class PardusMirror(models.Model):
    name = models.CharField('Sunucu adı', maxlength = 64, blank = False, unique = True)
    url = models.CharField('Adres', maxlength = 128)
    status = models.BooleanField('Aktif')

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'url')
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        verbose_name = "Pardus Yansısı"
        verbose_name_plural = "Pardus Yansıları"

#======
# Forms
#======

class RegisterForm(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı', max_length=30, help_text='En az 3, en fazla 30 karakter')
    firstname = forms.CharField(label='İsim', max_length=30)
    lastname = forms.CharField(label='Soyisim', max_length=30)
    email = forms.EmailField(label='E-Posta')
    password = forms.CharField(label='Parola', max_length=32, widget=forms.PasswordInput,)
    password_again = forms.CharField(label='Parola (tekrar)', max_length=32, widget=forms.PasswordInput, help_text='En az 5 karakter')
    city = forms.ChoiceField(label='Şehir', choices=CITY_LIST)
    homepage = forms.URLField(label='Web Sayfası', verify_exists=False, required=False, help_text='(zorunlu değil)')
    contributes = forms.ModelMultipleChoiceField(label='Katkı Başlıkları', queryset=Contribute.objects.all(), required=False, help_text='Bize nasıl katkıda bulunabilirsiniz? (ctrl ile birden fazla seçim yapılabilir, zorunlu değil)')
    contributes_summary = forms.CharField(label='Açıklama', widget=forms.Textarea, required=False, help_text='Katkı sağlayabilecekseniz açıklama yazın (zorunlu değil)')

    def clean_username(self):
        field_data = self.clean_data['username']

        if not field_data:
            return ''

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(u"Kullanıcı adında boşluk olmamalıdır")

        if len(field_data) < 3:
            raise forms.ValidationError(u"Kullanıcı adı en az 3 karakter olmalıdır")

        regexp = re.compile("\w+")
        if not regexp.match(field_data):
            raise forms.ValidationError(u"Kullanıcı adı geçersiz")

        ignored = IgnoredUsername.objects.filter(name__iexact=field_data)
        if len(ignored) > 0:
            raise forms.ValidationError(u"Bu kullanıcı adının alınması yasaklanmış")

        u = User.objects.filter(username__iexact=field_data)
        if len(u) > 0:
            raise forms.ValidationError(u"Bu kullanıcı adı daha önce alınmış")

        return self.clean_data['username']


    def clean_password_again(self):
        field_data = self.clean_data['password_again']
        password = self.clean_data['password']
        if not field_data:
            return ''

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

        if len(field_data) < 5:
            raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

        if (password or field_data) and password != field_data:
                    raise forms.ValidationError(u"Parolalar eşleşmiyor")

        return field_data

class ProfileEditForm(forms.Form):
    firstname = forms.CharField(label='İsim', max_length=30)
    lastname = forms.CharField(label='Soyisim', max_length=30)
    email = forms.EmailField(label='E-posta')
    city = forms.ChoiceField(label='Şehir', choices=CITY_LIST)
    homepage = forms.URLField(label='Ana Sayfa', required=False, help_text='http:// ile başlamayı unutmayın')
    old_password = forms.CharField(label='Eski Parola', widget=forms.PasswordInput, max_length=32, required=False)
    password = forms.CharField(label='Parola', widget=forms.PasswordInput, max_length=32, required=False, help_text='Değiştirmek istiyorsanız her ikisini de doldurun')
    password_again = forms.CharField(label='Parola (yeniden)', widget=forms.PasswordInput, max_length=32, required=False)
    show_email = forms.BooleanField(label='E-posta Adresini Göster', required=False, help_text='Profil sayfasında diğerleri e-posta adresinizi görsün mü?')

    def set_user(self, user):
        self.user = user

    def clean_old_password(self):
        field_data = self.clean_data['old_password']
        if not field_data:
            return ''
        else:
            if len(field_data.split(' ')) != 1:
                raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

            if len(field_data) < 5:
                raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

            return field_data

    def clean_password(self):
        field_data = self.clean_data['password']
        if not field_data:
            return ''
        else:
            if len(field_data.split(' ')) != 1:
                raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

            if len(field_data) < 5:
                raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

            return field_data

    def clean_password_again(self):
        field_data = self.clean_data['password_again']
        password = self.clean_data['password']
        old_password = self.clean_data['old_password']

        if old_password or password or field_data:
            if field_data and password and old_password:
                if len(field_data.split(' ')) != 1:
                    raise forms.ValidationError(u"Parolada boşluk olmamalıdır")

                if len(field_data) < 5:
                    raise forms.ValidationError(u"Parola en az 5 karakter olmalıdır")

                if (password or field_data) and password != field_data:
                    raise forms.ValidationError(u"Parolalar eşleşmiyor")

                u = User.objects.get(username=self.user.username)
                if not u.check_password(old_password):
                    raise forms.ValidationError(u"Eski parola yanlış")

                return field_data
            else:
                raise forms.ValidationError(u"Parolayı değiştirmek için her 3 alanı da doldurun")
        else:
            return ''
