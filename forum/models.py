#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from oi.middleware import threadlocals
from oi.st.tags import Tag
from oi.poll.models import Poll

from oi.forum.settings import FORUM_FROM_EMAIL

import md5
from django.utils.translation import ugettext as _

class Post(models.Model):
    """
    Post model.

    __unicode__: id of post
    get_absolute_url: absolute url of post
    save(): saves post and updates Topic and Forum objects
    """
    topic = models.ForeignKey('Topic', verbose_name=_('Topic'))
    author = models.ForeignKey(User, verbose_name=_('Author'))
    text = models.TextField(verbose_name=_('Post'))
    hidden = models.BooleanField(blank=True, null=True, default=0, verbose_name=_('Hidden'))
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=_('Create date'))
    edited = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=_('Update date'))
    edit_count = models.IntegerField(default=0, verbose_name=_('Number of updates'))
    last_edited_by = models.ForeignKey(User, blank=True, null=True, related_name='last edited by', verbose_name=_('Last Editor'))
    ip = models.IPAddressField(blank=True, verbose_name=_('IP address'))

    def __unicode__(self):
        return "%s" % self.id

    def get_absolute_url(self):
        """Use topic/forum.get_latest_post_url whenever you can"""
        # all the mess is about pages
        import oi.forum.settings

        posts = self.topic.post_set.all().order_by('created')

        # binary search position of this post
        i = 0
        j = int(self.topic.posts)
        k = (i + j) / 2
        while i < j:
            k = (i + j) / 2
            if self.id > posts[k].id:
                i = k + 1
            else:
                j = k
        page = i / oi.forum.settings.POSTS_PER_PAGE + 1

        return '/forum/%s/%s/?page=%s#post%s' % (self.topic.forum.slug, self.topic.id, page, self.id)

    def get_quote_url(self):
        return '/forum/%s/%s/quote/%s/' % (self.topic.forum.slug, self.topic.id, self.id)

    def get_edit_url(self):
        """ returns topic edit url of the post """
        return '/forum/%s/%s/edit/%s/' % (self.topic.forum.slug, self.topic.id, self.id)

    def get_hide_url(self):
        return '/forum/%s/%s/hide/%s/' % (self.topic.forum.slug, self.topic.id, self.id)

    def get_delete_url(self):
        return '/forum/%s/%s/delete/%s/' % (self.topic.forum.slug, self.topic.id, self.id)

    def get_delete_confirm_url(self):
        return '/forum/%s/%s/delete/%s/yes/' % (self.topic.forum.slug, self.topic.id, self.id)

    # creates unique message id for each post. This is used by "Message-ID" header.
    def get_email_id(self):
        return '<%s.%s@%s>' % (self.id, self.author.username, FORUM_FROM_EMAIL.split('@')[1])

    def get_abuse_report_url(self):
        return "/forum/raporla/%s/" % self.id

    class Admin:
        list_display = ('id', 'topic', 'author', 'created', 'ip')

    class Meta:
        ordering = ('-edited',)
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        permissions = (
                       ("can_see_post_ip", _("Can see author ip")),
                       ("can_hide_post", _("Can hide")),
                       ("can_see_hidden_posts", _("Can see hidden posts")),
                      )

    def save(self):
        new_post = False

        if not self.id:
            new_post = True

        if not self.ip:
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
            f = Forum.objects.get(id=self.topic.forum.id)
            t = Topic.objects.get(id=self.topic.id)

            posts=t.post_set.all().order_by('-created')

            #if the latest post is the one we are deleting
            if posts[0].id == self.id :
                #if there are more than one topic we should prevent the disaster othewise let it go :)
                if posts.count()>1:
                    latest_post=posts[1]
                else:
                    latest_post=posts[0]

            else : #if we dont delete the latest one the last one is suitable
                latest_post=posts[0]

            #latest_post = t.post_set.all().order_by('-created')[0].id

            t.topic_latest_post = latest_post
            t.posts -= 1
            t.save()

            f.forum_latest_post = latest_post
            f.posts -= 1
            f.save()

        super(Post, self).delete()

class Topic(models.Model):
    """
    Topic model.
    """
    forum = models.ForeignKey('Forum', verbose_name=_('Forum'))
    title = models.CharField(max_length=100, verbose_name=_('Topic'))
    sticky = models.BooleanField(blank=True, null=True, default=0, verbose_name=_('Sticy'))
    locked = models.BooleanField(blank=True, null=True, default=0, verbose_name=_('Locked'))
    hidden = models.BooleanField(blank=True, null=True, default=0, verbose_name=_('Hidden'))
    posts = models.IntegerField(default=0, verbose_name=_('Number of posts'))
    views = models.IntegerField(default=0, verbose_name=_('Number of views'))
    topic_latest_post = models.ForeignKey(Post, blank=True, null=True, related_name='topic_latest_post', verbose_name=_('Latest posts'))
    tags = models.ManyToManyField(Tag, verbose_name=_('Tags'))
    poll = models.ForeignKey(Poll, blank=True, null=True, verbose_name=_("Poll"))

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/forum/%s/%s/?page=1' % (self.forum.slug, self.id)

    def get_latest_post_url(self):
        import oi.forum.settings
        lastpage = ((self.posts - 1) / oi.forum.settings.POSTS_PER_PAGE) + 1
        return '/forum/%s/%s/?page=%s#post%s' % (self.forum.slug, self.id, lastpage, self.topic_latest_post.id)

    def get_follow_url(self):
        return '/forum/%s/%s/follow' % (self.forum.slug, self.id)

    def get_reply_url(self):
        return '/forum/%s/%s/reply/' % (self.forum.slug, self.id)

    def get_merge_url(self):
        return '/forum/%s/%s/merge/' % (self.forum.slug, self.id)

    def get_move_url(self):
        return '/forum/%s/%s/move/' % (self.forum.slug, self.id)

    def get_edit_url(self):
        return '/forum/%s/%s/edit/' % (self.forum.slug, self.id)

    def get_stick_url(self):
        return '/forum/%s/%s/stick/' % (self.forum.slug, self.id)

    def get_lock_url(self):
        return '/forum/%s/%s/lock/' % (self.forum.slug, self.id)

    def get_hide_url(self):
        return '/forum/%s/%s/hide/' % (self.forum.slug, self.id)

    def get_create_poll_url(self):
        return '/forum/%s/%s/poll/create/' % (self.forum.slug, self.id)

    def get_change_poll_url(self):
        return '/forum/%s/%s/poll/change/' % (self.forum.slug, self.id)

    def get_delete_poll_url(self):
        return '/forum/%s/%s/poll/delete/' % (self.forum.slug, self.id)

    def get_email_id(self):
        return '<%s.%s@%s>' % (md5.new(self.title).hexdigest(), self.id, FORUM_FROM_EMAIL.split('@')[1])

    # <a title="...."> for tooltip. Just get a short context of first post on the topic.
    def get_tooltip_context(self):
        from django.utils.html import strip_tags

        posts = Post.objects.filter(topic=self)
        # we should get the last element of an array
        # negative indexing is not supported so we just get it through "post.count()-1"
        context = strip_tags(posts[posts.count()-1].text)

        if len(context) > 160:
            # if it has more than 160 chars, append "..." to the end
            return context[:160] + '...'
        else:
            return context

    class Admin:
        list_display = ('forum', 'title', 'sticky', 'locked', 'hidden')

    class Meta:
        ordering = ('-sticky', '-topic_latest_post')
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        permissions = (
                       ("can_hide_topic", _("Can hide topic")),
                       ("can_stick_topic", _("Can stick topic")),
                       ("can_lock_topic", _("Can lock topic")),
                       ("can_tag_topic", _("Can tag topic")),
                       ("can_see_hidden_topics", _("Can see hidden topics")),
                       ("can_merge_topic", _("Can merge topic")),
                       ("can_move_topic", _("Can move topic")),
                       ("can_create_poll", _("Can create poll")),
                       ("can_change_poll", _("Can change poll")),
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
    category = models.ForeignKey('Category', null=True, verbose_name=_('Category'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    slug = models.SlugField(verbose_name=_('SEF name'))
    description = models.TextField(verbose_name=_('Description'))
    hidden = models.BooleanField(blank=True, null=True, default=0, verbose_name=_('Hidden'))
    locked = models.BooleanField(blank=True, null=True, default=0, verbose_name=_('Locked'))
    topics = models.IntegerField(default=0, verbose_name=_('Number of topics'))
    posts = models.IntegerField(default=0, verbose_name=_('Number of posts'))
    forum_latest_post = models.ForeignKey(Post, blank=True, null=True, related_name='forum_latest_post', verbose_name=_('Latest Post'))
    order = models.PositiveIntegerField(verbose_name=_('Ordering'))

    def get_absolute_url(self):
        return '/forum/%s/' % self.slug

    def get_latest_post_url(self):
        import oi.forum.settings

        latest_topic = self.forum_latest_post.topic
        lastpage = ((latest_topic.posts - 1) / oi.forum.settings.POSTS_PER_PAGE) + 1
        return '/forum/%s/%s/?page=%s#post%s' % (self.slug, latest_topic.id, lastpage, self.forum_latest_post.id)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('order',)
        unique_together = (('category', 'order'),)
        verbose_name = _('Forum')
        verbose_name_plural = _('Forums')
        permissions = (
                       ("can_hide_forum", _("Can hide forum")),
                       ("can_lock_forum", _("Can lock forum")),
                       ("can_see_hidden_forums", _("Can see hidden forums")),
                      )

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Kategory name'))
    hidden = models.BooleanField(blank=True, null=True, verbose_name=_('Hidden'))
    order = models.PositiveIntegerField(unique=True, verbose_name=_('Ordering'))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/forum/'

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        permissions = (
                       ("can_hide_category", _("Can hide category")),
                       ("can_see_hidden_categories", _("Can see hidden categories")),
                      )

class AbuseReport(models.Model):
    post = models.ForeignKey(Post, verbose_name=_('Post'))
    submitter = models.ForeignKey(User, verbose_name=_('Reporter'))
    reason = models.TextField(max_length=512, blank=False, verbose_name=_("Reason"))

    class Admin:
        list_display = ('post', 'submitter')

    class Meta:
        verbose_name = _('Abuse Report')
        verbose_name_plural = _('Abuse Reports')

class WatchList(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    topic = models.ForeignKey(Topic, verbose_name=_('Topic'))

    def __unicode__(self):
        return '%s' % self.topic.title

    class Admin:
        pass

    class Meta:
        verbose_name = _('Watchlist')
        verbose_name_plural = _('Watchlists')
