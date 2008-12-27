#!/usr/bin/python
# -*- coding: utf-8 -*-

from hashlib import md5

from django import template
from django.template import Library

# We call it avatar_url instead of gravatar_url so if we change services in the
# future it's just a change of the tag.

register = Library()

@register.simple_tag
def avatar_url(email, size=50, rating='g', default=None):
    """
    Returns a gravatar url.

    Example tag usage: {% avatar user.email 80 "g" %}

    :Parameters:
       - `email`: the email to send to gravatar.
       - `size`: optional YxY size for the image.
       - `rating`: optional rating (g, pg, r, or x) of the image.
       - `default`: optional default image url or hosted image like wavatar.
    """
    # Verify the rating actually is a rating accepted by gravatar
    rating = rating.lower()
    ratings = ['g', 'pg', 'r', 'x']
    if rating not in ratings:
        raise template.TemplateSyntaxError('rating must be %s' % (
            ", ".join(ratings)))
    # Create and return the url
    hash = md5(email).hexdigest()
    url = 'http://www.gravatar.com/avatar/%s?s=%s&r=%s' % (
        hash, size, rating)
    if default:
        url = "%s&d=%s" % (url, default)
    return url
