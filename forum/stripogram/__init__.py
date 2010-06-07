# Copyright (c) 2001 Chris Withers
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: __init__.py,v 1.11 2003/01/07 10:57:21 fresh Exp $

from html2text import HTML2Text
from html2safehtml import HTML2SafeHTML

def html2text(s, ignore_tags=(), indent_width=4, page_width=80):
    ignore_tags = [t.lower() for t in ignore_tags]
    parser = HTML2Text(ignore_tags, indent_width, page_width)
    parser.feed(s)
    parser.close()
    parser.generate()
    return parser.result

def html2safehtml(s, valid_tags=('b', 'a', 'i', 'br', 'p')):
    valid_tags = [t.lower() for t in valid_tags]
    parser = HTML2SafeHTML(valid_tags)
    parser.feed(s)
    parser.close()
    parser.cleanup()
    return parser.result

try:
    from AccessControl import ModuleSecurityInfo
except ImportError:
    # no Zope around
    pass
else:
    ModuleSecurityInfo('Products.stripogram').declareObjectPublic()
    ModuleSecurityInfo('Products.stripogram').declarePublic('html2text', 'html2safehtml')
