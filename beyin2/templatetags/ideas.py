#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.template import Library
from django.template.defaultfilters import truncatewords_html

from oi.beyin2.models import Idea, Category, Status
IDEAS_IN_HOMEPAGE = 5

register = Library()

@register.simple_tag
def idea_list():
    ideas = Idea.objects.filter(is_hidden=False ).order_by('-id')[:IDEAS_IN_HOMEPAGE]
    html = ''
    for idea in ideas:
        description = truncatewords_html(idea.description, 20)
        html += '<div class="idea"><p class="title"><a href="%s">%s</a></p><p class="description">%s</p></div>' % (idea.get_absolute_url(), idea.title, description)
    return html

@register.simple_tag
def category_list():
    categories = Category.objects.all()
    html = ""
    for category in categories:
        html += "<li><a href=\"%s\" title=\"%s\">%s</a></li>" % (
                category.get_absolute_url(),
                category.name,
                category.name,
                )
    return html

@register.simple_tag
def status_list():
    statuses = Status.objects.all()
    html = ""
    for status in statuses:
        html += "<li><a href=\"%s\" title=\"%s\">%s</a></li>" % (
                status.get_absolute_url(),
                status.name,
                status.name,
                )
    return html

