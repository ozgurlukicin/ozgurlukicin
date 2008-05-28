#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Uğur Çetin
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.


from django import template
from oi.tema.models import Category

register = template.Library()

class CategoryBox(template.Node):
    def __init__(self, categories):
        self.categories = ""
        for category in categories:
            self.categories += """<li><a href="%s">%s</a></li>\n                """ % (category.get_absolute_url(), category.name)

    def render(self, content):
        return """
        <div class="sidebar_box">
            <div class="sidebar_top">&nbsp;</div>
            <div class="sidebar_middle">
                <h2>Kategoriler</h2>
                <ul>
                %s
                </ul>
            </div>
            <div class="sidebar_bottom">&nbsp;</div>
        </div>
""" % self.categories

@register.tag
def category_box(parser, token):
    """ returns a petition box for oi sidebar """
    return CategoryBox(Category.objects.all())
