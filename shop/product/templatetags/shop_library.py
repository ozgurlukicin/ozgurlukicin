#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from elementtree.ElementTree import Element, SubElement, tostring
from django.template import Library

from oi.shop.product.models import Category, Product
from oi.shop.cart.views import get_cart_for_user, get_cart_html

register = Library()

def recurse_for_children(current_node, parent_node, active_cat, show_empty=True):
    child_count = current_node.child.count()

    if show_empty or child_count > 0 or current_node.product_set.count() > 0:
        temp_parent = SubElement(parent_node, 'li')
        attrs = {'href': current_node.get_absolute_url()}
        if current_node == active_cat:
            attrs["class"] = "current"
        if current_node.parent:
             link = SubElement(temp_parent, 'a', attrs)
        else:
             link = SubElement(temp_parent, 'span', {})
        link.text = current_node.name

        if child_count > 0:
            new_parent = SubElement(temp_parent, 'ul')
            children = current_node.child.all()
            for child in children:
                recurse_for_children(child, new_parent, active_cat)

@register.simple_tag
def category_tree(id=None):
    """
    Creates an unnumbered list of the categories.  For example:
    <ul>
        <li>Books
            <ul>
            <li>Science Fiction
                <ul>
                <li>Space stories</li>
                <li>Robot stories</li>
                </ul>
            </li>
            <li>Non-fiction</li>
            </ul>
    </ul>
    """
    active_cat = None
    if id:
        active_cat = Category.objects.get(id=id)
    root = Element("ul")
    for cats in Category.objects.filter(parent__isnull=True):
        recurse_for_children(cats, root, active_cat)
    return tostring(root, 'utf-8')

@register.simple_tag
def get_cart(user):
    cart = get_cart_for_user(user)
    return get_cart_html(cart)
