#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime
from django.template import Library
from django.utils.timesince import timesince

register = Library()

#@register.inclusion_tag('forum/pagination.html', takes_context=True)
#def paginator(context, adjacent_pages=2):
    #"""
    #To be used in conjunction with the object_list generic view.

    #Adds pagination context variables for use in displaying first, adjacent and
    #last page links in addition to those created by the object_list generic
    #view.
    #"""
    #page_numbers = [n for n in \
                    #range(context['page'] - adjacent_pages, context['page'] + adjacent_pages + 1) \
                    #if n > 0 and n <= context['pages']]
    #return {
        #'hits': context['hits'],
        #'results_per_page': context['results_per_page'],
        #'page': context['page'],
        #'pages': context['pages'],
        #'page_numbers': page_numbers,
        #'next': context['next'],
        #'previous': context['previous'],
        #'has_next': context['has_next'],
        #'has_previous': context['has_previous'],
        #'show_first': 1 not in page_numbers,
        #'show_last': context['pages'] not in page_numbers,
    #}

@register.filter
def timedelta(value, arg=None):
    if not value:
        return ''
    if arg:
        cmp = arg
    else:
        cmp = datetime.now()
    if value > cmp:
        return "%s sonra" % timesince(cmp,value)
    else:
        return "%s önce" % timesince(value,cmp)