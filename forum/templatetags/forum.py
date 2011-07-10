#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import template
from django.template import Context, loader
from oi.forum.models import Topic

register = template.Library()

@register.simple_tag
def forum_sidebar():
    latest_topics = Topic.objects.filter(topic_latest_post__hidden=False, forum__is_published=True, forum__hidden=False).order_by("topic_latest_post").distinct()[:10]
    html = ''
    for topic in latest_topics:
        html += '<div class="idea"><p class="title"><a href="%s">%s</a></p></div>' % (topic.get_latest_post_url(), topic.title)
    return html
