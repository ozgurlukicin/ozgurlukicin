# -*- coding: utf-8 -*-

"""
feedjack
Gustavo Picón
urls.py
"""

from django.conf.urls.defaults import patterns

urlpatterns = patterns('oi.feedjack.views',
    (r'^user/(?P<feedUser>\d+)/tag/(?P<tag>.*)/$', 'mainview'),
    (r'^user/(?P<feedUser>\d+)/$', 'mainview'),
    (r'^tag/(?P<tag>.*)/$', 'mainview'),

    #(r'^opml/$', opml),
    #(r'^foaf/$', foaf),
    (r'^$', 'mainview'),
)
