''' 
Copyright (c) 2005, the Lawrence Journal-World
All rights reserved.

Modified by PreFab Software, Inc.
'''


from django.conf import settings
from blogmaker.comments.models import Comment
from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site

class LatestCommentsFeed(Feed):
    "Feed of latest comments on the current site."

    comments_class = Comment

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "%s comments" % self._site.name.title()

    def link(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "http://%s/" % (self._site.domain)

    def description(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "Latest comments on %s" % self._site.name.title()

    def items(self):
        return self.comments_class.objects.filter(site__pk=settings.SITE_ID, is_public=True)[:40]
