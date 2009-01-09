#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
feedjack
Gustavo Picón
update_feeds.py
"""

import os
import time
import optparse
import datetime
import socket
import traceback
import sys

import feedparser

VERSION = '0.9.10'
URL = 'http://www.feedjack.org/'
USER_AGENT = 'Feedjack %s - %s' % (VERSION, URL)

def encode(tstr):
    """ Encodes a unicode string in utf-8
    """
    if not tstr:
        return ''
    # this is _not_ pretty, but it works
    try:
        return tstr.encode('utf-8', "xmlcharrefreplace")
    except UnicodeDecodeError:
        # it's already UTF8.. sigh
        return tstr.decode('utf-8').encode('utf-8')

def mtime(ttime):
    """ datetime auxiliar function.
    """
    return datetime.datetime.fromtimestamp(time.mktime(ttime))

def get_tags(entry):
    """ Returns a list of tag objects from an entry.
    """
    from oi.feedjack import models

    fcat = []
    if entry.has_key('tags'):
        for tcat in entry.tags:
            if tcat.label != None:
                term = tcat.label
            else:
                term = tcat.term
            qcat = encode(term).strip()
            if ',' in qcat or '/' in qcat:
                qcat = qcat.replace(',', '/').split('/')
            else:
                qcat = [qcat]
            for zcat in qcat:
                tagname = zcat.lower()
                while '  ' in tagname:
                    tagname = tagname.replace('  ', ' ')
                tagname = tagname.strip()
                if not tagname or tagname == ' ':
                    continue
                if not models.Tag.objects.filter(name=tagname):
                    cobj = models.Tag(name=tagname)
                    cobj.save()
                fcat.append(models.Tag.objects.get(name=tagname))
    return fcat

def get_entry_data(entry, feed, options):
    """ Retrieves data from a post and returns it in a tuple.
    """
    try:
        link = encode(entry.link)
    except AttributeError:
        link = feed.link
    try:
        title = encode(entry.title)
    except AttributeError:
        title = link
    guid = encode(entry.get('id', title))

    if entry.has_key('author_detail'):
        author = encode(entry.author_detail.get('name', ''))
        author_email = encode(entry.author_detail.get('email', ''))
    else:
        author, author_email = '', ''

    if not author:
        author = encode(entry.get('author', entry.get('creator', '')))
    if not author_email:
        author_email = 'nospam@nospam.com'

    try:
        content = encode(entry.content[0].value)
    except:
        content = encode(entry.get('summary', entry.get('description', '')))


    # Patch for resizing images, Eren Turkay <turkay.eren@gmail.com>
    # 2007-07-01

    from django.conf import settings

    if settings.FEEDJACK_RESIZE_IMAGE:

        from BeautifulSoup import BeautifulSoup
        import tempfile, urllib2
        from PIL import Image

        global USER_AGENT

        soup = BeautifulSoup(content)
        images = soup.findAll("img")
        if len(images) > 0:
            for img in images:
                # get image src and split the last value of /
                url = img.get("src")
                image_name = url.split("/")[-1]

                # create a request and get the image data
                if options.verbose:
                    print '  RESIZE: Getting %s to resize' % url
                req = urllib2.Request(url)
                req.add_header('User-Agent', USER_AGENT)
                image_data = urllib2.urlopen(req).read()

                # write it
                tmp = tempfile.mktemp()
                file = open(tmp, 'w')
                file.write(image_data)
                file.close()

                im = Image.open(tmp, 'r')
                # we'll do it respecting aspect ratio
                resize_x = im.size[0]
                resize_y = im.size[1]

                if settings.FEEDJACK_MAX_IMAGE_X and resize_x > settings.FEEDJACK_MAX_IMAGE_X:
                    resize_y = int(settings.FEEDJACK_MAX_IMAGE_X * 1.0 / resize_x * resize_y)
                    resize_x = settings.FEEDJACK_MAX_IMAGE_X

                if settings.FEEDJACK_MAX_IMAGE_Y and resize_y > settings.FEEDJACK_MAX_IMAGE_Y:
                    resize_x = int(settings.FEEDJACK_MAX_IMAGE_Y * 1.0 / resize_y * resize_x)
                    resize_y = settings.FEEDJACK_MAX_IMAGE_Y

                # if there is a change on images, continue the process
                if im.size[0] != resize_x or im.size[1] != resize_y:
                    res = im.resize((resize_x, resize_y), Image.ANTIALIAS)
                    res.save("%s/%s" % (settings.FEEDJACK_UPLOAD_DIR, image_name))

                    # generate a site url that will be showed in feedjack index and replace it with original
                    resized_image_url = "%s/%s" % (settings.FEEDJACK_UPLOAD_URL, image_name)
                    img['src'] = resized_image_url

                    # if it has width
                    if img.has_key("width"):
                        img['width'] = resize_x

                    # if it has height
                    if img.has_key("height"):
                        img['height'] = resize_y

                    content = soup
                    if options.verbose:
                        print '  RESIZE: Image resized %s, %s' % (url, resized_image_url)
                else:
                    if options.verbose:
                        print '  RESIZE: Skipped, there is no change\n'

                try:
                    os.unlink(tmp)
                except:
                    pass
            # endpatch

    if entry.has_key('modified_parsed'):
        date_modified = mtime(entry.modified_parsed)
    else:
        date_modified = None

    fcat = get_tags(entry)
    comments = encode(entry.get('comments', ''))

    return (link, title, guid, author, author_email, content, date_modified, \
      fcat, comments)

def process_entry(entry, fpf, feed, postdict, options):
    """ Process a post in a feed and saves it in the DB if necessary.
    """
    from oi.feedjack import models

    (link, title, guid, author, author_email, content, date_modified, fcat, \
      comments) = get_entry_data(entry, feed, options)

    if options.verbose:
        print 'entry:'
        print '  title:', title
        print '  link:', link
        print '  guid:', guid
        print '  author:', author
        print '  author_email:', author_email
        print '  tags:', [tcat.name for tcat in fcat]

    if guid in postdict:
        tobj = postdict[guid]
        if options.verbose:
            print '  - Existing previous post object, updating..'
        postdict[guid] = tobj
        if tobj.content != content or \
          (date_modified and tobj.date_modified != date_modified):
            if options.verbose:
                print '  - Post has changed, updating...'
            if not date_modified:
                # damn non-standard feeds
                date_modified = tobj.date_modified
            tobj.title = title
            tobj.link = link
            tobj.content = content
            tobj.guid = guid
            tobj.date_modified = date_modified
            tobj.author = author
            tobj.author_email = author_email
            tobj.comments = comments
            tobj.tags.clear()
            [tobj.tags.add(tcat) for tcat in fcat]
            tobj.save()
        elif options.verbose:
            print '  - Post has not changed, ignoring.'
    else:
        if options.verbose:
            print '  - Creating post object...'
        if not date_modified:
            # if the feed has no date_modified info, we use the feed mtime or
            # the current time
            if fpf.feed.has_key('modified_parsed'):
                date_modified = mtime(fpf.feed.modified_parsed)
            elif fpf.has_key('modified'):
                date_modified = mtime(fpf.modified)
            else:
                date_modified = datetime.datetime.now()
        tobj = models.Post(feed=feed, title=title, link=link,
            content=content, guid=guid, date_modified=date_modified,
            author=author, author_email=author_email,
            comments=comments)
        tobj.save()
        [tobj.tags.add(tcat) for tcat in fcat]

def process_feed(feed, options):
    """ Downloads and parses a feed.
    """
    from oi.feedjack import models

    if options.verbose:
        print '#\n# Processing feed (%d):' % feed.id, feed.feed_url, '\n#'
    else:
        print '# Processing feed (%d):' % feed.id, feed.feed_url

    # we check the etag and the modified time to save bandwith and avoid bans
    try:
        fpf = feedparser.parse(feed.feed_url, agent=USER_AGENT,
            etag=feed.etag)
    except:
        print '! ERROR: feed cannot be parsed'
        return 1

    if hasattr(fpf, 'status'):
        if options.verbose:
            print 'fpf.status:', fpf.status
        if fpf.status == 304:
            # this means the feed has not changed
            if options.verbose:
                print 'Feed has not changed since last check, ignoring.'
            return 2

        if fpf.status >= 400:
            # http error, ignore
            print '! HTTP ERROR'
            return 3

    if hasattr(fpf, 'bozo') and fpf.bozo and options.verbose:
        print '!BOZO'

    # the feed has changed (or it is the first time we parse it)
    # saving the etag and last_modified fields
    feed.etag = encode(fpf.get('etag', ''))
    try:
        feed.last_modified = mtime(fpf.modified)
    except:
        pass

    feed.title = encode(fpf.feed.get('title', ''))[0:254]
    feed.tagline = encode(fpf.feed.get('tagline', ''))
    feed.link = encode(fpf.feed.get('link', ''))
    feed.last_checked = datetime.datetime.now()

    if options.verbose:
        print 'feed.title', feed.title
        print 'feed.tagline', feed.tagline
        print 'feed.link', feed.link
        print 'feed.last_checked', feed.last_checked

    guids = []
    for entry in fpf.entries:
        if encode(entry.get('id', '')):
            guids.append(encode(entry.get('id', '')))
        elif entry.title:
            guids.append(encode(entry.title))
        elif entry.link:
            guids.append(encode(entry.link))
    feed.save()
    if guids:
        postdict = dict([(post.guid, post) \
          for post in models.Post.objects.filter(feed=feed.id).filter(guid__in=guids)])
    else:
        postdict = {}

    for entry in fpf.entries:
        try:
            process_entry(entry, fpf, feed, postdict, options)
        except:
            (etype, eobj, etb) = sys.exc_info()
            print '! -------------------------'
            print traceback.format_exception(etype, eobj, etb)
            traceback.print_exception(etype, eobj, etb)
            print '! -------------------------'

    feed.save()

    return 0

def update_feeds(options):
    """ Updates all active feeds.
    """
    from oi.feedjack import models

    #for feed in models.Feed.objects.filter(is_active=True).iterator():
    for feed in models.Feed.objects.filter(is_active=True):
        try:
            process_feed(feed, options)
        except:
            (etype, eobj, etb) = sys.exc_info()
            print '! -------------------------'
            print traceback.format_exception(etype, eobj, etb)
            traceback.print_exception(etype, eobj, etb)
            print '! -------------------------'

def main():
    """ Main function. Nothing to see here. Move along.
    """
    parser = optparse.OptionParser(usage='%prog [options]', version=USER_AGENT)
    parser.add_option('--settings', \
      help='Python path to settings module. If this isn\'t provided, the DJANGO_SETTINGS_MODULE enviroment variable will be used.')
    parser.add_option('-f', '--feed', action='append', type='int', \
      help='A feed id to be updated. This option can be given multiple times to update several feeds at the same time (-f 1 -f 4 -f 7).')
    parser.add_option('-s', '--site', type='int', \
      help='A site id to update.')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', \
      default=False, help='Verbose output.')
    parser.add_option('-t', '--timeout', type='int', default=10, \
      help='Wait timeout in seconds when connecting to feeds.')
    options = parser.parse_args()[0]
    if options.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = options.settings

    from oi.feedjack import models, fjcache

    # settting socket timeout (default= 10 seconds)
    socket.setdefaulttimeout(options.timeout)

    if options.feed:
        for feed in options.feed:
            try:
                process_feed(models.Feed.objects.get(pk=feed), options)
            except  models.Feed.DoesNotExist:
                print '! Unknown feed id: ', feed
    elif options.site:
        feeds = [sub.feed \
          for sub in \
          models.Site.objects.get(pk=int(options.site)).subscriber_set.all()]
        for feed in feeds:
            try:
                process_feed(feed, options)
            except  models.Feed.DoesNotExist:
                print '! Unknown site id: ', feed
    else:
        update_feeds(options)

    # removing the cached data in all sites, this will only work with the
    # memcached, db and file backends
    [fjcache.cache_delsite(site.id) for site in models.Site.objects.all()]

if __name__ == '__main__':
    main()

#~
