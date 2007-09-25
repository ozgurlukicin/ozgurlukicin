#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from oi.middleware import threadlocals
from oi.st.models import Tag

class Post(models.Model):
    """
    Post model.

    __str__: id of post
    get_absolute_url: absolute url of post
    save(): saves post and updates Topic and Forum objects
    """
    topic = models.ForeignKey('Topic', verbose_name='Konu')
    author = models.ForeignKey(User, verbose_name='Yazar')
    text = models.TextField(verbose_name='İleti')
    hidden = models.BooleanField(blank=True, null=True, default=0, verbose_name='Gizli')
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name='Oluşturulma tarihi')
    update = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name='Güncellenme tarihi')
    update_count = models.IntegerField(default=0, verbose_name='Güncellenme sayısı')
    ip = models.IPAddressField(blank=True, verbose_name='IP adresi')

    def __str__(self):
        return "%s" % self.id

    def get_absolute_url(self):
        return '/forum/%s/%s/#post%s' % (self.topic.forum.slug, self.topic.id, self.id)

    def get_quote_url(self):
        return '/forum/%s/%s/quote/%s/' % (self.topic.forum.slug, self.topic.id, self.id)

    def get_edit_url(self):
        return '/forum/%s/%s/edit/%s/' % (self.topic.forum.slug, self.topic.id, self.id)

    def get_hide_url(self):
        return '/forum/%s/%s/hide/%s/' % (self.topic.forum.slug, self.topic.id, self.id)

    def get_delete_url(self):
        return '/forum/%s/%s/delete/%s/' % (self.topic.forum.slug, self.topic.id, self.id)

    def get_delete_confirm_url(self):
        return '/forum/%s/%s/delete/%s/yes/' % (self.topic.forum.slug, self.topic.id, self.id)

    class Admin:
        list_display = ('id', 'topic', 'author', 'created', 'ip')

    class Meta:
        ordering = ('-update',)
        verbose_name = 'İleti'
        verbose_name_plural = 'İletiler'
        permissions = (
                       ("can_hide", "Can hide"),
                       ("can_see_hidden_posts", "Can see hidden posts"),
                      )

    def save(self):
        if not self.id:
            new_post = True
        else:
            #self.update_count += 1
            new_post = False

        self.ip = threadlocals.get_current_ip()
        super(Post, self).save()

        if new_post:
            t = Topic.objects.get(pk=self.topic.id)
            t.topic_latest_post_id = self.id
            t.posts += 1
            t.save()

            f = Forum.objects.get(pk=self.topic.forum.id)
            f.forum_latest_post_id = self.id
            f.posts += 1
            f.save()

    def delete(self):
        if self.id:
            t = Topic.objects.get(id=self.topic.id)
            #FIXME: set the latest post after deletion
            #t.topic_latest_post_id = self.id
            t.posts -= 1
            t.save()

            f = Forum.objects.get(id=self.topic.forum.id)
            #FIXME: set the latest post after deletion
            #f.forum_latest_post_id = self.id
            f.posts -= 1
            f.save()

        super(Post, self).delete()

class Topic(models.Model):
    """
    Topic model.
    """
    forum = models.ForeignKey('Forum', verbose_name='Forum')
    title = models.CharField(maxlength=100, verbose_name='Başlık')
    sticky = models.BooleanField(blank=True, null=True, default=0, verbose_name='Sabit')
    locked = models.BooleanField(blank=True, null=True, default=0, verbose_name='Kilitli')
    hidden = models.BooleanField(blank=True, null=True, default=0, verbose_name='Gizli')
    posts = models.IntegerField(default=0, verbose_name='İleti sayısı')
    views = models.IntegerField(default=0, verbose_name='Görüntülenme sayısı')
    topic_latest_post = models.ForeignKey(Post, blank=True, null=True, related_name='topic_latest_post', verbose_name='Son ileti')
    tags = models.ManyToManyField(Tag, verbose_name='Etiketler')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/forum/%s/%s/' % (self.forum.slug, self.id)

    def get_reply_url(self):
        return '/forum/%s/%s/reply/' % (self.forum.slug, self.id)

    def get_edit_url(self):
        return '/forum/%s/%s/edit/' % (self.forum.slug, self.id)

    def get_stick_url(self):
        return '/forum/%s/%s/stick/' % (self.forum.slug, self.id)

    def get_lock_url(self):
        return '/forum/%s/%s/lock/' % (self.forum.slug, self.id)

    def get_hide_url(self):
        return '/forum/%s/%s/hide/' % (self.forum.slug, self.id)

    def get_delete_url(self):
        return '/forum/%s/%s/delete/' % (self.forum.slug, self.id)

    def get_delete_url(self):
        return '/forum/%s/%s/delete/yes/' % (self.forum.slug, self.id)

    class Admin:
        list_display = ('forum', 'title', 'sticky', 'locked', 'hidden')

    class Meta:
        ordering = ('-sticky', '-topic_latest_post')
        verbose_name = 'Konu'
        verbose_name_plural = 'Konular'
        permissions = (
                       ("can_hide", "Can hide"),
                       ("can_stick", "Can stick"),
                       ("can_lock", "Can lock"),
                       ("can_tag", "Can tag"),
                       ("can_see_hidden_topics", "Can see hidden topics"),
                      )

    def save(self):
        if not self.id:
            f = Forum.objects.get(id=self.forum.id)
            f.topics += 1
            f.save()
        super(Topic, self).save()

    def delete(self):
        if self.id:
            f = Forum.objects.get(id=self.forum.id)
            f.topics -= 1
            f.posts -= self.posts
            f.save()
        super(Topic, self).delete()

class Forum(models.Model):
    category = models.ForeignKey('Category', null=True, verbose_name='Kategori')
    name = models.CharField(maxlength=100, verbose_name='İsim')
    slug = models.SlugField(prepopulate_from=('name',), verbose_name='SEF isim')
    description = models.TextField(verbose_name='Açıklama')
    hidden = models.BooleanField(blank=True, null=True, default=0, verbose_name='Gizli')
    locked = models.BooleanField(blank=True, null=True, default=0, verbose_name='Kapalı')
    topics = models.IntegerField(default=0, verbose_name='Konu sayısı')
    posts = models.IntegerField(default=0, verbose_name='İleti sayısı')
    forum_latest_post = models.ForeignKey(Post, blank=True, null=True, related_name='forum_latest_post', verbose_name='Son ileti')
    order = models.PositiveIntegerField(verbose_name='Sıralama')

    def get_absolute_url(self):
        return '/forum/%s/' % self.slug

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('category', 'name')

    class Meta:
        ordering = ('order',)
        unique_together = (('category', 'order'),)
        verbose_name = 'Forum'
        verbose_name_plural = 'Forumlar'
        permissions = (
                       ("can_hide", "Can hide"),
                       ("can_lock", "Can lock"),
                       ("can_see_hidden_forums", "Can see hidden forums"),
                      )

class Category(models.Model):
    name = models.CharField(maxlength=255, verbose_name='Kategori ismi')
    hidden = models.BooleanField(blank=True, null=True, verbose_name='Gizli')
    order = models.PositiveIntegerField(verbose_name='Sıralama')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/forum/'

    class Admin:
        list_display = ('id', 'name')
        ordering = ['-name']
        search_fields = ['name']

    class Meta:
        ordering = ['name']
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        permissions = (
                       ("can_hide", "Can hide"),
                       ("can_see_hidden_categories", "Can see hidden categories"),
                      )

class AbuseReport(models.Model):
    post = models.ForeignKey(Post, verbose_name='İleti')
    submitter = models.ForeignKey(User, verbose_name='Raporlayan kullanıcı')

    class Admin:
        list_display = ('post', 'submitter')

    class Meta:
        verbose_name = 'İleti şikayeti'
        verbose_name_plural = 'İleti şikayetleri'

class WatchList(models.Model):
    user = models.ForeignKey(User, verbose_name='Kullanıcı')
    topic = models.ForeignKey(Topic, verbose_name='Konu')

    class Admin:
        pass

    class Meta:
        verbose_name = 'İzleme listesi'
        verbose_name_plural = 'İzleme listeleri'