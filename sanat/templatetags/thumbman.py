#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

""" image related filters """

##################################################
## DEPENDENCIES ##

from django import template
from django.template import TemplateSyntaxError
from oi.sanat.utils import make_thumbnail, get_image_size
register = template.Library()
##################################################
## FILTERS ##
DEFAULT_HEIGHT=100
DEFAULT_WIDTH=100

def thumbnail(url, args=''):
    """ Returns thumbnail URL and create it if not already exists.

.. note:: requires PIL_,
    if PIL_ is not found or thumbnail can not be created returns original URL.

.. _PIL: http://www.pythonware.com/products/pil/

Usage::

    {{ url|thumbnail:"width=10,height=20" }}
    {{ url|thumbnail:"width=10" }}
    {{ url|thumbnail:"height=20" }}

Parameters:

width
    requested image width

height
    requested image height

Image is **proportionally** resized to dimension which is no greather than ``width x height``.

Thumbnail file is saved in the same location as the original image
and his name is constructed like this::

    %(dirname)s/%(basename)s_t[_w%(width)d][_h%(height)d].%(extension)s

or if only a width is requested (to be compatibile with admin interface)::

    %(dirname)s/%(basename)s_t%(width)d.%(extension)s

"""

    kwargs = {}
    if args:
        if ',' not in args:
            # ensure at least one ','
            args += ','
        for arg in args.split(','):
            arg = arg.strip()
            if arg == '': continue
            kw, val = arg.split('=', 1)
            kw = kw.lower()
            try:
                val = int(val) # convert all ints
            except ValueError:
                raise template.TemplateSyntaxError, "thumbnail filter: argument %r is invalid integer (%r)" % (kw, val)
            kwargs[kw] = val
        # for
    #

    if ('width' not in kwargs) and ('height' not in kwargs):
		kwargs['width']=DEFAULT_WIDTH
		kwargs['height']=DEFAULT_HEIGHT
		#raise template.TemplateSyntaxError, "thumbnail filter requires arguments (width and/or height)"

    ret = make_thumbnail(url, **kwargs)
    if ret is None:
        return url
    else:
        return ret


register.filter('thumbnail', thumbnail)
