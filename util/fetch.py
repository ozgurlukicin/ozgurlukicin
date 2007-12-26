''' Copyright (c) 2006-2007, PreFab Software Inc. '''


''' Utilities for fetching data from URLs '''

import datetime, gzip, re, urllib, urllib2, urlparse
import cStringIO as StringIO

from oi.util.feedparser import _parse_date, _FeedURLHandler

debuglevel=0

# This finds meta-refresh with time < 10 seconds
refreshRe = re.compile(r'''http-equiv=['"]refresh['"]\s+content=['"]\d;\s*url=\s*([^'"\s]+)['"]''', re.IGNORECASE)

def read_html(url, etag=None, modified=None, agent=''):
    ''' Open and read data from a URL.
        Returns both the connection object and the data.
        Will follow some <meta> tag redirects.
    '''
    tried = set([url])
    f, data = read_resource(url, etag, modified, agent)
    while True:
        m = refreshRe.search(data)
        if not m:
            break
            
        redirectUrl = m.group(1)
        if redirectUrl == '/nojs.htm':  # yuck; special case for jacklewis.net
            break
            
        url = urlparse.urljoin(f.url, redirectUrl)
        if url in tried:
            break
        tried.add(url)
        
        f, data = read_resource(url, etag, modified, agent)
        if not hasattr(f, 'status'):
            f.status = 301  # Treat a <meta> redirect as permanent

    return f, data
    

def read_resource(url, etag=None, modified=None, agent='', isFeed=False):
    ''' Open and read data from a URL.
        Returns both the connection object and the data.
        Arguments are the same as for open_resource().
    '''
    f = open_resource(url, etag, modified, agent, isFeed)
    try:
        data = f.read()
        f.close()
    except ValueError, e:
        # This is a workaround for a very specific problem
        # Some web sites do not correctly chunk HTTP 1.1 data
        # urllib2 can't deal with them; it raises a ValueError
        # Catch the error and try urllib instead
        # The returned file object is not as rich as the one returned
        # by open_resource() but it does have info()
        if e.message != "invalid literal for int() with base 16: ''":
            raise
        f = urllib.urlopen(url)
        data = f.read()
        f.close()
    
    # Even though we ask for no encoding, some sites still return gzip
    # http://hughhewitt.townhall.com/blog is one
    if f.info().get('content-encoding', None) == 'gzip':
        data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
    
    return f, data
        

def open_resource(url, etag=None, modified=None, agent='', isFeed=False):
    """URL --> stream

    If the etag argument is supplied, it will be used as the value of an
    If-None-Match request header.

    If the modified argument is supplied, it will be used
    as the value of an If-Modified-Since request header.

    If the agent argument is supplied, it will be used as the value of a
    User-Agent request header.

    Loosely based on feedparser._open_resource()
    """

    # try to open with urllib2 (to use optional headers)
    request = urllib2.Request(url)
    request.add_header('User-Agent', agent)
    if etag:
        request.add_header('If-None-Match', etag)

    if modified:
        request.add_header('If-Modified-Since', modified)
    
    request.add_header('Accept-encoding', '')

    if isFeed:
        request.add_header('A-IM', 'feed') # RFC 3229 support

    # Use _FeedURLHandler to capture redirect codes in f.status
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=debuglevel), _FeedURLHandler())

    opener.addheaders = [] # RMK - must clear so we only send our custom User-Agent
    try:
        f = opener.open(request)
        return f
    finally:
        opener.close() # JohnD

 
