#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.template import Library
from django.conf import settings

from urlgrabber.grabber import urlopen, URLGrabError
from stat import *
import md5
import os
import time

GRAVATAR_URL = "http://www.gravatar.com/avatar"
GRAVATAR_SERVER_TIMEOUT = 2

# We will check if user has gravatar account according to this hash
# NOTE:
# This hash is for 100px default image. If you happen to use different resolution by default, you should change the hash.
# We're using 100px avatars by default.
GRAVATAR_DEFAULT_IMAGE_HASH = "e2deb22899972ac721b862f9c8e73ef1"

# the path cache files are stored.
CACHE_PATH = "%s/tmp" % settings.DOCUMENT_ROOT
# cache suffix, for look&feel thingy :) I don't the way when only hashes are listen when I look at tmp dir :P
CACHE_SUFFIX = "gravatar"
# Our cache is valid for 1.5 hours
CACHE_TIMEOUT = 5400

class Gravatar:
    """
    # Caching stuff:
    # 1- Check if we already checked out user's gravatar
    # 2- If the file exists, look up its content. It will either 1 or 0 so as to explain whether it's default gravatar image or not.
    # 3- If doesn't exist, check out the avatar and write the hash of user's email as filename
    # 4- If it's default gravatar image (content is 0), just return user's avatar on the site
    # 5- If content is 1, return gravatar URL directly,
    # 6- Finally, check the file's creation date. If 1 hour lasted, delete it. This means our cache machanism last for 1 hour :)
    """
    def __init__(self):
        self.userObject = None
        self.image_size = None
        # holds user's email hash as md5, used by cache mechanism
        self.email_hash = None
        self.cache_file = None
        self.gravatar_image_url = None

    # creates cache and writes the data in it.
    def create_cache(self, data):
        file = open(self.cache_file, "w")
        file.write(data)
        file.close()

    def is_cached(self):
        """Check if the user's avatar is cached"""
        if os.path.exists(self.cache_file):
            return True
        else:
            return False

    def is_cache_expired(self):
        """We keep our cache valid for 1.5 hours."""
        last_modified = os.stat(self.cache_file)[ST_MTIME]

        if (time.time() - last_modified) > CACHE_TIMEOUT:
            return True
        else:
            return False

    def has_gravatar_account(self):
        if open(self.cache_file).read() == "1":
            return True
        else:
            return False

    # It's like a constructor. We will mainly fill "userObject" and "image_size" variables for the use of CACHE functions
    def get_gravatar_image(self, userObject, image_size=100):
        self.userObject = userObject
        self.image_size = image_size
        self.email_hash = md5.md5(userObject.email).hexdigest()
        self.cache_file = "%s/%s-%s" % (CACHE_PATH, CACHE_SUFFIX, self.email_hash)
        self.gravatar_image_url = "%s/%s?s=%s" % (GRAVATAR_URL, self.email_hash, image_size)

        # have we checked the image for user already?
        if not self.is_cached():
            try:
                connection = urlopen(self.gravatar_image_url, timeout=GRAVATAR_SERVER_TIMEOUT)
                image = connection.read()
                connection.close()

                # if it's default image, write 0 to cache file
                if md5.md5(image).hexdigest() == GRAVATAR_DEFAULT_IMAGE_HASH:
                    self.create_cache("0")
                    return self.userObject.get_profile().avatar.file.url
                else:
                    self.create_cache("1")
                    return self.gravatar_image_url
            except URLGrabError:
                # gravatar connection error
                self.create_cache("0")
                return self.userObject.get_profile().avatar.file.url
        else:
            # if our cache is expired, delete the file and recall this function.
            if self.is_cache_expired():
                os.remove(self.cache_file)
                self.get_gravatar_image(userObject, image_size)

            # if it's cached and the user has gravatar account, return gravatar URL.
            # if not, you know what to do :)
            if self.has_gravatar_account():
                return self.gravatar_image_url
            else:
                return self.userObject.get_profile().avatar.file.url

gravatar = Gravatar()
register = Library()
register.simple_tag(gravatar.get_gravatar_image)
