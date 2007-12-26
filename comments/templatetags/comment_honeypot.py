'''
Template tag to support comments honeypots as described in
http://www.nedbatchelder.com/text/stopbots.html

Notes on caching:
Ned Batchelder's honeypot includes the IP address of the request in the spinner.
The spinner is included in a hidden form field. When the form is submitted, the
spinner is re-computed and checked against the submitted value. If they differ, the
submission is considered to be spam.

This will not work if the comment form is cached - each request gets the same spinner,
from the cache, and the following submission will be rejected because it comes from a 
different IP address.

Possible solutions:
- Don't include the IP address in the spinner by setting CHECK_IP to False
- Don't cache the page containing the comment form

If CHECK_IP is False, the timestamp still protects against replaying a particular post.
Of course the time stamp is cached as well, so your cache timeout must be significantly
less than the comment timeout (comments.views.MAX_COMMENT_TIME).

Copyright (c) 2006-2007, PreFab Software Inc.

Copyright (c) 2005, the Lawrence Journal-World
All rights reserved.  
'''

import time
#from hashlib import md5
import sha

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

#ip icin ekledik bunu
from oi.middleware import threadlocals

register = template.Library()
    
#: Flag for whether to check the poster's IP address or not
# Turn this OFF if your comment form will be cached in any way
CHECK_IP = False

@register.tag
def comment_form(parser, token):
    """ Honeypot version of free_comment_form. Implements the ideas here:
        http://www.nedbatchelder.com/text/stopbots.html
        Does not support the options of free_comment_form.
        Displays a comment form for the given params.

    Syntax::

        {% comment_form for [pkg].[py_module_name] [context_var_containing_obj_id] %}

    Example usage::

        {% comment_form for lcom.eventtimes event.id %}

    ``[context_var_containing_obj_id]`` can be a hard-coded integer or a variable containing the ID.
    """
    tokens = token.contents.split()
    if len(tokens) != 4:
        raise template.TemplateSyntaxError, "%r tag requires at least 3 arguments" % tokens[0]
    if tokens[1] != 'for':
        raise template.TemplateSyntaxError, "Second argument in %r tag must be 'for'" % tokens[0]
    try:
        package, module = tokens[2].split('.')
    except ValueError: # unpack list of wrong size
        raise template.TemplateSyntaxError, "Third argument in %r tag must be in the format 'package.module'" % tokens[0]
    try:
        content_type = ContentType.objects.get(app_label__exact=package, model__exact=module)
    except ContentType.DoesNotExist:
        raise template.TemplateSyntaxError, "%r tag has invalid content-type '%s.%s'" % (tokens[0], package, module)

    obj_id_lookup_var, obj_id = None, None
    if tokens[3].isdigit():
        obj_id = tokens[3]
        try: # ensure the object ID is valid
            content_type.get_object_for_this_type(pk=obj_id)
        except ObjectDoesNotExist:
            raise template.TemplateSyntaxError, "%r tag refers to %s object with ID %s, which doesn't exist" % (tokens[0], content_type.name, obj_id)
    else:
        obj_id_lookup_var = tokens[3]
    return CommentFormNode(content_type, obj_id_lookup_var, obj_id)


class CommentFormNode(template.Node):
    def __init__(self, content_type, obj_id_lookup_var, obj_id):
        self.content_type = content_type
        self.obj_id_lookup_var, self.obj_id = obj_id_lookup_var, obj_id

    def render(self, context):
        context.push()
        if self.obj_id_lookup_var is not None:
            try:
                self.obj_id = template.resolve_variable(self.obj_id_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''
            # Validate that this object ID is valid for this content-type.
            # We only have to do this validation if obj_id_lookup_var is provided,
            # because comment_form() validates hard-coded object IDs.
            try:
                self.content_type.get_object_for_this_type(pk=self.obj_id)
            except ObjectDoesNotExist:
                context['display_form'] = False
            else:
                context['display_form'] = True
        else:
            context['display_form'] = True
        context['target'] = '%s:%s' % (self.content_type.id, self.obj_id)

        # Honeypot fields and field name map
        context['timestamp'] = timestamp = str(int(time.time()))
        context['spinner'] = spinner = makeSpinner(timestamp, threadlocals.get_current_ip(), context['target'])
        context['fields'] = makeFieldNames(spinner)
        context['previewText'] = 'Preview comment'
        
        default_form = template.loader.get_template('comments/comment_form.html')
        output = default_form.render(context)
        context.pop()
        return output


def makeSpinner(timestamp, ip, obj_id):
    ''' This is the key used to hash the field names '''
    spinner = timestamp + obj_id + settings.SECRET_KEY
    if CHECK_IP:
        spinner += ip
    return sha.new(spinner).hexdigest()


def makeFieldNames(spinner):
    ''' Returns a dict mapping cleartext field names to hashed field names.
        The actual form will use the hashed names.
    '''
    fields = 'comment person_email person_name person_www post preview submit target timestamp'.split()
    fields += 'honeypot1 honeypot2 honeypot3 honeypot4'.split()
    names = dict((name, sha.new(name+spinner+settings.SECRET_KEY).hexdigest()) for name in fields)
    return names
