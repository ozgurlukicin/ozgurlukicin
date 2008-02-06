
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from oi.settings import MEDIA_ROOT,MEDIA_URL
from django.core.cache import get_cache
from django.db.models.fields import FileField
import Image
import re, os, urlparse, fnmatch
import shutil, os

#use local cache thing
image_cache = get_cache('locmem:///')

#is it alot ?
_FILE_CACHE_TIMEOUT = 60 * 60 * 60 * 24 # 1 day
_THUMBNAIL_GLOB = '%s_t*%s'

#some value not important for now
DEFAULT_HEIGHT=100
DEFAULT_WIDTH=100

def _get_thumbnail_path(path, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
	""" create thumbnail path from path and required width and/or height.
	thumbnail file name is constructed like this:
    <basename>_t_[w<width>][_h<height>].<extension>"""

	basedir = os.path.dirname(path) + '/'
	base, ext = os.path.splitext(os.path.basename(path))

	# make thumbnail filename
	th_name = base + '_t'

	if (width is not None) and (height is not None):
		th_name += '_w%d_h%d' % (width, height)

	elif width is not None:
		th_name += '%d' % width # for compatibility with admin

	elif height is not None:
		th_name += '_h%d' % height

	th_name += ext

	return urlparse.urljoin(basedir, th_name)
#

def _get_path_from_url(url, root=MEDIA_ROOT, url_root=MEDIA_URL):
    """ make filesystem path from url """

    if url.startswith(url_root):
        url = url[len(url_root):] # strip media root url

    return os.path.normpath(os.path.join(root, url))
#

def _get_url_from_path(path, root=MEDIA_ROOT, url_root=MEDIA_URL):
    """ make url from filesystem path """

    if path.startswith(root):
        path = path[len(root):] # strip media root

    return urlparse.urljoin(root, path.replace('\\', '/'))
#

def _has_thumbnail(photo_url, width=None, height=None, root=MEDIA_ROOT, url_root=MEDIA_URL):
    # one of width/height is required
    #assert (width is not None) or (height is not None)

	#if we just want to get a default one
	if not width and not height:
		place=_get_path_from_url(photo_url)

		if place:
			import fnmatch, os
    		base, ext = os.path.splitext(os.path.basename(place))
    		basedir = os.path.dirname(place)
    		for file in fnmatch.filter(os.listdir(basedir), _THUMBNAIL_GLOB % (base, ext)):
				#if it comes here it has a thumbnail
				return True


		else:
			return False

	else:
		import os
		return os.path.isfile(_get_path_from_url(_get_thumbnail_path(photo_url, width, height), root, url_root))

def model_has_thumbnail(model):
	""" To see if given model has a thumbnail"""
	for obj in model._meta.fields:
		if isinstance(obj, FileField):
			x=getattr(obj,'file')
			if x :
				x=_get_url_from_path(x)
				return _has_thumbnail(x)

			else:
				return False


def make_thumbnail(photo_url, width=DEFAULT_HEIGHT, height=DEFAULT_WIDTH, root=MEDIA_ROOT, url_root=MEDIA_URL):
    """ create thumbnail """

    # one of width/height is required
    assert (width is not None) or (height is not None)

    if not photo_url: return None

    th_url = _get_thumbnail_path(photo_url, width, height)
    th_path = _get_path_from_url(th_url, root, url_root)
    photo_path = _get_path_from_url(photo_url, root, url_root)

    if _has_thumbnail(photo_url, width, height, root, url_root):
        # thumbnail already exists
        if not (os.path.getmtime(photo_path) > os.path.getmtime(th_path)):
            # if photo mtime is newer than thumbnail recreate thumbnail
            return th_url

    # make thumbnail

    # get original image size
    orig_w, orig_h = get_image_size(photo_url, root, url_root)
    if (orig_w is None) and (orig_h) is None:
        # something is wrong with image
        return photo_url

    # make proper size
    if (width is not None) and (height is not None):
        if (orig_w == width) and (orig_h == height):
            # same dimensions
            return None
        size = (width, height)
    elif width is not None:
        if orig_w == width:
            # same dimensions
            return None
        size = (width, orig_h)
    elif height is not None:
        if orig_h == height:
            # same dimensions
            return None
        size = (orig_w, height)

    try:
        img = Image.open(photo_path).copy()
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(th_path)
    except Exception, err:
        # this goes to webserver error log
        #import sys
        #print >>sys.stderr, '[MAKE THUMBNAIL] error %s for file %r' % (err, photo_url)
        return photo_url

    return th_url
#

def _remove_thumbnails(photo_url, root=MEDIA_ROOT, url_root=MEDIA_URL):
	if not photo_url: return # empty url
	file_name = _get_path_from_url(photo_url, root, url_root)
	import fnmatch, os
	base, ext = os.path.splitext(os.path.basename(file_name))
	basedir = os.path.dirname(file_name)


	for file in fnmatch.filter(os.listdir(basedir), _THUMBNAIL_GLOB % (base, ext)):

		path = os.path.join(basedir, file)
		os.remove(path)
		image_cache.delete(path) # delete from cache


def remove_model_thumbnails(model):

	""" remove all thumbnails for all ImageFields (and subclasses) in the model """
	for obj in model._meta.fields:
		#print obj
		if isinstance(obj, FileField):
			url = getattr(model,'file')
			_remove_thumbnails(url)
    #
#

def _make_admin_thumbnail(url):
    """ make thumbnails for admin interface """
    make_thumbnail(url, width=120)
#

def make_admin_thumbnails(model):
    """ create thumbnails for admin interface for all ImageFields (and subclasses) in the model """

    for obj in model._meta.fields:
        if isinstance(obj, FileField):
            url = getattr(model,'file')
            make_thumbnail(url, width=120)
    #
#

def _get_thumbnail_url(photo_url, width=DEFAULT_HEIGHT, height=DEFAULT_WIDTH, root=MEDIA_ROOT, url_root=MEDIA_URL):
    """ return thumbnail URL for requested photo_url and required width and/or height

        if thumbnail file do not exists returns original URL
    """

    # one of width/height is required
    assert (width is not None) or (height is not None)

    if _has_thumbnail(photo_url, width, height, root, url_root):
        return _get_thumbnail_path(photo_url, width, height)
    else:
        return photo_url
#

def _set_cached_file(path, value):
    """ Store file dependent data in cache.
        Timeout is set to _FILE_CACHE_TIMEOUT (1month).
    """

    mtime = os.path.getmtime(path)
    image_cache.set(path, (mtime, value,), _FILE_CACHE_TIMEOUT)
#

def _get_cached_file(path, default=None):
    """ Get file content from cache.
        If modification time differ return None and delete
        data from cache.
    """

    cached = image_cache.get(path, default)
    if cached is None:
        return None
    mtime, value = cached

    if (not os.path.isfile(path)) or (os.path.getmtime(path) != mtime): # file is changed or deleted
        image_cache.delete(path) # delete from cache
        # remove thumbnails if exists
        base, ext = os.path.splitext(os.path.basename(path))
        basedir = os.path.dirname(path)
        for file in fnmatch.filter(os.listdir(basedir), _THUMBNAIL_GLOB % (base, ext)):
            os.remove(os.path.join(basedir, file))
        return None
    else:
        return value
#

def get_image_size(photo_url, root=MEDIA_ROOT, url_root=MEDIA_URL):
    """ returns image size.

        image sizes are cached (using separate locmem:/// cache instance)
    """

    path = os.path.join(root, _get_path_from_url(photo_url, root, url_root))

    size = _get_cached_file(path)
    if size is None:
        try:
            size = Image.open(path).size
        except Exception, err:
            # this goes to webserver error log
            #import sys
            #print >>sys.stderr, '[GET IMAGE SIZE] error %s for file %r' % (err, photo_url)
            return None, None
        #
        if size is not None:
            _set_cached_file(path, size)
        else:
            return None, None
    #
    return size
#
