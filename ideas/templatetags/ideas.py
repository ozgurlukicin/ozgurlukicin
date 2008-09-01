#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Uğur Çetin
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.template import Library
from oi.ideas.models import Idea
from oi.ideas.settings import IDEAS_IN_HOMEPAGE

register = Library()

@register.simple_tag
def idea_list():
    ideas = Idea.objects.filter(is_hidden=False).order_by('-id')[:IDEAS_IN_HOMEPAGE]
    html = ''
    for idea in ideas:
        html += '<div class="leftcolumn_content"><p class="title"><a href="%s">%s</a></p><p>%s</p></div>' % (idea.get_absolute_url(), idea.description)
    return html
