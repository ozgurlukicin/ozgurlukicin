# -*- coding: utf-8 -*-
# pylint: disable-msg=W0232, R0903, W0131

"""
feedjack
Gustavo Picón
models.py
"""

from django.db import models

from oi.feedjack import fjcache

SITE_ORDERBY_CHOICES = (
    (1, 'Date published.'),
    (2, 'Date the post was first obtained.')
)

class Link(models.Model):
    name = models.CharField('name', max_length=100, unique=True)
    link = models.URLField('link', verify_exists=True)

    class Meta:
        verbose_name = 'link'
        verbose_name_plural = 'links'

    class Admin:
        pass

    def __str__(self):
        return '%s (%s)' % (self.name, self.link)


class Site(models.Model):
    name = models.CharField('name', max_length=100)
    url = models.CharField('url', max_length=100, unique=True, \
      help_text='Example' + ': http://www.planetexample.com, ' \
        'http://www.planetexample.com:8000/foo')
    title = models.CharField('title', max_length=200)
    description = models.TextField('description')
    welcome = models.TextField('welcome', null=True, blank=True)
    greets = models.TextField('greets', null=True, blank=True)

    default_site = models.BooleanField('default site', default=False)
    posts_per_page = models.IntegerField('posts per page', default=20)
    order_posts_by = models.IntegerField('order posts by', default=1, \
      choices=SITE_ORDERBY_CHOICES)
    tagcloud_levels = models.IntegerField('tagcloud level', default=5)
    show_tagcloud = models.BooleanField('show tagcloud', default=True)

    use_internal_cache = models.BooleanField('use internal cache', default=True)
    cache_duration = models.IntegerField('cache duration', default=60*60*24, \
      help_text='Duration in seconds of the cached pages and data.')

    links = models.ManyToManyField(Link, verbose_name='links', filter_interface=models.VERTICAL, \
      null=True, blank=True)
    template = models.CharField('template', max_length=100, null=True, blank=True, \
      help_text='This template must be a directory in your feedjack ' \
        'templates directory. Leave blank to use the default template.')

    class Admin:
        list_display = ('url', 'name')

    class Meta:
        verbose_name = 'site'
        verbose_name_plural = 'sites'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self):
        if not self.template:
            self.template = 'default'
        # there must be only ONE default site
        defs = Site.objects.filter(default_site=True)
        if not defs:
            self.default_site = True
        elif self.default_site:
            for tdef in defs:
                if tdef.id != self.id:
                    tdef.default_site = False
                    tdef.save()
        self.url = self.url.rstrip('/')
        fjcache.hostcache_set({})
        super(Site, self).save()



class Feed(models.Model):
    feed_url = models.URLField('feed url', unique=True)

    name = models.CharField('name', max_length=100)
    shortname = models.CharField('shortname', max_length=50)
    is_active = models.BooleanField('is active', default=True, \
      help_text='If disabled, this feed will not be further updated.')

    title = models.CharField('title', max_length=200, blank=True)
    tagline = models.TextField('tagline', blank=True)
    link = models.URLField('link', blank=True)

    # http://feedparser.org/docs/http-etag.html
    etag = models.CharField('etag', max_length=50, blank=True)
    last_modified = models.DateTimeField('last modified', null=True, blank=True)
    last_checked = models.DateTimeField('last checked', null=True, blank=True)

    class Admin:
        list_display = ('name', 'feed_url', 'title', 'last_modified', \
          'is_active')
        fields = (
          (None, {'fields':('feed_url', 'name', 'shortname', 'is_active')}),
          ('Fields updated automatically by Feedjack', {
            'classes':'collapse',
            'fields':('title', 'tagline', 'link', 'etag', 'last_modified', \
              'last_checked')})
        )
        search_fields = ['feed_url', 'name', 'title']

    class Meta:
        verbose_name = 'feed'
        verbose_name_plural = 'feeds'
        ordering = ('name', 'feed_url',)

    def __str__(self):
        return '%s (%s)' % (self.name, self.feed_url)

    def save(self):
        super(Feed, self).save()

class Tag(models.Model):
    name = models.CharField('name', max_length=50, unique=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self):
        super(Tag, self).save()

class Post(models.Model):
    feed = models.ForeignKey(Feed, verbose_name='feed', null=False, blank=False)
    title = models.CharField('title', max_length=255)
    link = models.URLField('link', )
    content = models.TextField('content', blank=True)
    date_modified = models.DateTimeField('date modified', null=True, blank=True)
    guid = models.CharField('guid', max_length=200, db_index=True)
    author = models.CharField('author', max_length=50, blank=True)
    author_email = models.EmailField('author email', blank=True)
    comments = models.URLField('comments', blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='tags', filter_interface=models.VERTICAL)
    date_created = models.DateField('date created', auto_now_add=True)

    class Admin:
        list_display = ('title', 'link', 'author', 'date_modified')
        search_fields = ['link', 'title']
        date_hierarchy = 'date_modified'

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ('-date_modified',)
        unique_together = (('feed', 'guid'),)

    def __str__(self):
        return self.title

    def save(self):
        super(Post, self).save()

    def get_absolute_url(self):
        return self.link


class Subscriber(models.Model):
    site = models.ForeignKey(Site, verbose_name='site' )
    feed = models.ForeignKey(Feed, verbose_name='feed' )

    name = models.CharField('name', max_length=100, null=True, blank=True, \
      help_text='Keep blank to use the Feed\'s original name.')
    shortname = models.CharField('shortname', max_length=50, null=True, blank=True, \
      help_text='Keep blank to use the Feed\'s original shortname.')
    is_active = models.BooleanField('is active', default=True, \
      help_text='If disabled, this subscriber will not appear in the site or '\
        'in the site\'s feed.')

    class Admin:
        list_display = ('name', 'site', 'feed')
        list_filter = ('site',)

    class Meta:
        verbose_name = 'subscriber'
        verbose_name_plural = 'subscribers'
        ordering = ('site', 'name', 'feed')
        unique_together = (('site', 'feed'),)

    def __str__(self):
        return '%s in %s' % (self.feed, self.site)

    def get_cloud(self):
        from oi.feedjack import fjcloud
        return fjcloud.getcloud(self.site, self.feed.id)

    def save(self):
        if not self.name:
            self.name = self.feed.name
        if not self.shortname:
            self.shortname = self.feed.shortname
        super(Subscriber, self).save()


#~
