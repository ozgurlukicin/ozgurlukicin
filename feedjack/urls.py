# -*- coding: utf-8 -*-

"""
feedjack
Gustavo Picón
urls.py
"""

from django.conf.urls.defaults import patterns

urlpatterns = patterns('oi.feedjack.views',
    (r'^feed/rss/$', 'rssfeed'),
    (r'^feed/atom/$', 'atomfeed'),
    (r'^feed/$', 'rssfeed'),

    (r'^feed/atom/user/(?P<user>\d+)/tag/(?P<tag>.*)/$', 'atomfeed'),
    (r'^feed/atom/user/(?P<user>\d+)/$', 'atomfeed'),
    (r'^feed/atom/tag/(?P<tag>.*)/$', 'atomfeed'),
    (r'^feed/rss/user/(?P<user>\d+)/tag/(?P<tag>.*)/$', 'rssfeed'),
    (r'^feed/rss/user/(?P<user>\d+)/$', 'rssfeed'),
    (r'^feed/rss/tag/(?P<tag>.*)/$', 'rssfeed'),

    (r'^user/(?P<user>\d+)/tag/(?P<tag>.*)/$', 'mainview'),
    (r'^user/(?P<user>\d+)/$', 'mainview'),
    (r'^tag/(?P<tag>.*)/$', 'mainview'),

    #(r'^opml/$', opml),
    #(r'^foaf/$', foaf),
    (r'^$', 'mainview'),
)
