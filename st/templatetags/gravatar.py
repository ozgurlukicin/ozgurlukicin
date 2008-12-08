# -*- coding: utf-8 -*-

from django.template import Library
from urlgrabber import urlopen
import md5

GRAVATAR_URL = "http://www.gravatar.com/avatar"
TIMEOUT = 2

# We will check if user has gravatar account according to this hash
# NOTE!!! :
# This hash is for 100px default image. If you happen to use different resolution by default, you should change the hash.
# We're using 100px avatars by default.
GRAVATAR_DEFAULT_IMAGE_HASH = "e2deb22899972ac721b862f9c8e73ef1"

register = Library()

class Gravatar:
    def __init__(self):
        self.gravatar_image_data = None
        self.gravatar_image_url = None

    def get_gravatar_image_for_email(self, userEmail, size):
        self.gravatar_image_url = "%s/%s?s=%s" % (GRAVATAR_URL, md5.md5(userEmail).hexdigest(), size)

        try:
            image = urlopen(self.gravatar_image_url, timeout=TIMEOUT)
            self.gravatar_image_data = image.read()
            image.close()
        except:
            self.gravatar_image_data = None

    def have_gravatar(self):
        if self.gravatar_image_data == None or md5.md5(self.gravatar_image_data).hexdigest() == GRAVATAR_DEFAULT_IMAGE_HASH:
            return False
        else:
            return True

    # return image URL used for Avatar. If user has gravatar account, return gravatar URL.
    # If doesn't have, returns ordinary avatar within site
    def get_gravatar_image(self, UserObject, size=100):
        self.get_gravatar_image_for_email(UserObject.email, size)

        if self.have_gravatar():
            return self.gravatar_image_url
        else:
            return UserObject.get_profile().avatar.file.url

gravatar = Gravatar()
register.simple_tag(gravatar.get_gravatar_image)
