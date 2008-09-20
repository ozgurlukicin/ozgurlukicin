#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Uğur Çetin
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.template import Library
from django.template.defaultfilters import truncatewords_html

from oi.ideas.models import Idea
from oi.ideas.settings import IDEAS_IN_HOMEPAGE

register = Library()

@register.simple_tag
def idea_list():
    ideas = Idea.objects.filter(is_hidden=False).order_by('-id')[:IDEAS_IN_HOMEPAGE]
    html = ''
    for idea in ideas:
        description = truncatewords_html(idea.description, 22)
        html += '<div class="leftcolumn_content"><p class="title"><a href="%s">%s</a></p>%s</div>' % (idea.get_absolute_url(), idea.title, description)
    return html
