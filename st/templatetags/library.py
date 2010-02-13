# -*- coding: utf-8 -*-

import os, Image
from datetime import datetime
from django.template import Library
from django.utils.timesince import timesince
from oi.settings import MEDIA_ROOT, MEDIA_URL

from oi.forum.postmarkup import render_bbcode

register = Library()

@register.filter
def thumbnail(file, size='200x200'):
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    basename, format = file.rsplit('.', 1)
    miniature = basename + '_' + size + '.' +  format
    miniature_filename = os.path.join(MEDIA_ROOT, miniature)
    miniature_url = os.path.join(MEDIA_URL, miniature)
    filename = os.path.join(MEDIA_ROOT, file)
    if os.path.exists(filename):
        # if image has been modified, remove old thumbnail
        if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
            os.unlink(miniature_filename)
        # if the image wasn't already resized, resize it
        if not os.path.exists(miniature_filename):
            #print '>>> debug: resizing the image to the format %s!' % size
            image = Image.open(filename)
            image.thumbnail([x, y]) # generate a 200x200 thumbnail
            image.save(miniature_filename, image.format)
        return miniature_url
    else:
        return file

@register.filter
def renderbbcode(context):
    return render_bbcode(context)

@register.inclusion_tag('paginator.html', takes_context=True)
def paginator(context, adjacent_pages=4):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    page_numbers = [n for n in \
                    range(context['page'] - adjacent_pages, context['page'] + adjacent_pages + 1) \
                    if n > 0 and n <= context['pages']]
    return {
        'hits': context['hits'],
        'results_per_page': context['results_per_page'],
        'page': context['page'],
        'pages': context['pages'],
        'page_numbers': page_numbers,
        'next': context['next'],
        'previous': context['previous'],
        'has_next': context['has_next'],
        'has_previous': context['has_previous'],
        'show_first': 1 not in page_numbers,
        'show_last': context['pages'] not in page_numbers,
    }

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

@register.filter
def rfc822datetime(value):
    if value:
        rfc822days = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
        rfc822months = ("Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Oct", "Nov", "Dec")
        return "%s, %s %s %d %s:%s:%s +0200" % (rfc822days[value.isoweekday()], str(value.day).zfill(2), rfc822months[value.month-1], d.year, str(value.hour).zfill(2), str(value.minute).zfill(2), str(value.second).zfill(2))
    else:
        return ""
