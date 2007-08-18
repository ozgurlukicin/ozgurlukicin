#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

class Category(meta.Model):
    parent = meta.ForeignKey(self, null=True, blank=True, verbose_name='Ana kategori')
    name = meta.CharField(maxlength=255, verbose_name='Kategori ismi')

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('id', 'name')
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        ordering = ['name']
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

    def moderators(self):
        mod = Moderator.objects.filter(category=self.id)

        if mods.count() > 0:
            return ', '.join([m.user.username for m in mods])
        else:
            return None

class Forum(models.Model):
    category = meta.ForeignKey(Category, null=True, verbose_name='Kategori')
    name = models.CharField(maxlength=100, verbose_name='İsim')
    slug = models.SlugField(verbose_name='SEF isim')
    description = models.TextField(verbose_name='Açıklama')
    topics = models.IntegerField(default=0, verbose_name='Konu sayısı')
    posts = models.IntegerField(default=0, verbose_name='İleti sayısı')
    forum_latest_post = models.ForeignKey(Post, blank=True, null=True, related_name='forum_latest_post', verbose_name='Son ileti')

    def get_absolute_url(self):
        return '/forum/%s/' % self.slug

    def __str__(self):
        return self.title

    class Admin:
        pass

    class Meta:
        verbose_name = 'Forum'
        verbose_name_plural = 'Forumlar'

class Topic(models.Model):
    forum = models.ForeignKey(Forum, verbose_name='Forum')
    title = models.CharField(maxlength=100, verbose_name='Başlık')
    sticky = models.BooleanField(blank=True, null=True, verbose_name='Sabit')
    closed = models.BooleanField(blank=True, null=True, verbose_name='Kapalı')
    hidden = models.BooleanField(blank=True, null=True, verbose_name='Gizli')
    posts = models.IntegerField(default=0, verbose_name='İleti sayısı')
    views = models.IntegerField(default=0, verbose_name='Görüntülenme sayısı')
    thread_latest_post = models.ForeignKey(Post, blank=True, null=True, related_name='thread_latest_post', verbose_name='Son ileti')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/forum/%s/%s/' % (self.forum.slug, self.id)

    def save(self):
        if not self.id:
            f = Forum.objects.get(id=self.forum.id)
            f.threads += 1
            f.save()
        super(Topic, self).save()

    def delete(self):
        if self.id:
            f = Forum.objects.get(id=self.forum.id)
            f.threads -= 1
            f.save()
        super(Topic, self).delete()

    class Admin:
        pass

    class Meta:
        ordering = ('-sticky', '-thread_latest_post')

class Post(models.Model):
    topic = models.ForeignKey(Topic, verbose_name='Konu')
    author = models.ForeignKey(User, verbose_name='Yazar')
    text = models.TextField(verbose_name='İleti')
    update = models.DateTimeField(blank=True, null=True, verbose_name='Güncelleme tarihi')
    update_count = models.IntegerField(default=0, verbose_name='Güncelleme sayısı')
    ip = models.IPAddressField(blank=True, verbose_name='IP adresi')


    def __str__(self):
        return "%s" % self.id

    def get_absolute_url(self):
        return '/forum/%s/%s/#post%s' % (self.thread.forum.slug, self.thread.id, self.id)

    def save(self):
        new_post = False

        self.ip = threadlocals.get_current_ip()

        if not self.id:
            self.time = datetime.now()
            new_post = True

        super(Post, self).save()

        if new_post:
            t = Thread.objects.get(id=self.thread.id)
            t.thread_latest_post_id = self.id
            t.posts += 1
            t.save()

            f = Forum.objects.get(id=self.thread.forum.id)
            f.forum_latest_post_id = self.id
            f.posts += 1
            f.save()

    def delete(self):
        if self.id:
            t = Thread.objects.get(id=self.thread.id)
            #FIXME: set the latest post after deletion
            #t.thread_latest_post_id = self.id
            t.posts -= 1
            t.save()

            f = Forum.objects.get(id=self.thread.forum.id)
            #FIXME: set the latest post after deletion
            #f.forum_latest_post_id = self.id
            f.posts -= 1
            f.save()

        super(Post, self).delete()

    class Admin:
        pass

    class Meta:
        ordering = ('-update',)

class Moderator(models.Model):
    forum = models.ForeignKey(Forum, verbose_name='Forum')
    user = models.ForeignKey(User, verbose_name='Kullanıcı')

class AbuseReport(models.Model):
    post = models.ForeignKey(Post, verbose_name='İleti')
    submitter = models.ForeignKey(User, verbose_name='Raporlayan kullanıcı')

    class Admin:
        list_display = ('post', 'submitter')

class WatchList(models.Model):
    user = models.ForeignKey(User, verbose_name='Kullanıcı')
    topic = models.ForeignKey(Topic, verbose_name='Konu')

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True, editable=False, core=True, edit_inline=models.STACKED, max_num_in_admin=1)
    profile = models.TextField(blank=True)
    avatar = PhotoField(blank=True, upload_to='upload/avatars/', width=24, height=24)
    ppp = models.IntegerField(choices = ((5, '5'), (10, '10'), (20, '20'), (50, '50')), default = 20, help_text = "Posts per page")
    tpp = models.IntegerField(choices = ((5, '5'), (10, '10'), (20, '20'), (50, '50')), default = 20, help_text = "Threads per page")
    notify_email = models.BooleanField(default=False, blank=True, help_text = "Email notifications for watched discussions.")
    reverse_posts = models.BooleanField(default=False, help_text = "Display newest posts first.")

    class Admin:
        pass