"""
Template tags designed to work with applications which use comment
moderation.

Copyright (c) 2007, James Bennett
All rights reserved.

Copyright (c) 2005, the Lawrence Journal-World
All rights reserved.

Modified by PreFab Software, Inc.
"""

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_model
from django.contrib.contenttypes.models import ContentType

from oi.comments.models import Comment

register = template.Library()

@register.tag
def get_public_comment_list(parser, token):
    return _get_comment_list(parser, token, 'comment')

@register.tag
def get_public_trackback_list(parser, token):
    return _get_comment_list(parser, token, 'trackback')

def _get_comment_list(parser, token, comment_type):
    """
    Retrieves comments for a particular object and stores them in a
    context variable.

    The difference between this tag and Django's built-in comment list
    tags is that this tag will only return comments with
    ``is_public=True``. If your application uses any sort of comment
    moderation which sets ``is_public=False``, you'll probably want to
    use this tag, as it makes the template logic simpler by only
    returning approved comments.
    
    Syntax::
    
        {% get_public_comment_list for [app_name].[model_name] [object_id] as [varname] %}
    
        
    To retrieve comments in reverse order (e.g., newest comments
    first), pass 'reversed' as an extra argument after ``varname``.
    
    So, for example, to retrieve registered comments for a flatpage
    with ``id`` 12, use like this::
    
        {% get_public_comment_list for flatpages.flatpage 12 as comment_list %}
    
    
    To retrieve in reverse order (newest comments first)::
    
        {% get_public_comment_list for flatpages.flatpage 12 as comment_list reversed %}
        
    """
    bits = token.contents.split()
    if len(bits) not in (6, 7):
        raise template.TemplateSyntaxError("'%s' tag takes 5 or 6 arguments" % bits[0])
    if bits[1] != 'for':
        raise template.TemplateSyntaxError("first argument to '%s' tag must be 'for'" % bits[0])
    try:
        app_name, model_name = bits[2].split('.')
    except ValueError:
        raise template.TemplateSyntaxError("second argument to '%s' tag must be in the form 'app_name.model_name'" % bits[0])
    model = get_model(app_name, model_name)
    if model is None:
        raise template.TemplateSyntaxError("'%s' tag got invalid model '%s.%s'" % (bits[0], app_name, model_name))
    content_type = ContentType.objects.get_for_model(model)
    var_name, object_id = None, None
    if bits[3].isdigit():
        object_id = bits[3]
        try:
            content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            raise template.TemplateSyntaxError("'%s' tag got reference to %s object with id %s, which doesn't exist" % (bits[0], content_type.name, object_id))
    else:
        var_name = bits[3]
    if bits[4] != 'as':
        raise template.TemplateSyntaxError("fourth argument to '%s' tag must be 'as'" % bits[0])
    if len(bits) == 7:
        if bits[6] != 'reversed':
            raise template.TemplateSyntaxError("sixth argument to '%s' tag, if given, must be 'reversed'" % bits[0])
        ordering = '-'
    else:
        ordering = ''
    return PublicCommentListNode(app_name, model_name, var_name, object_id, bits[5], ordering, comment_type)


class PublicCommentListNode(template.Node):
    def __init__(self, package, module, context_var_name, obj_id, var_name, ordering, comment_type):
        self.package, self.module = package, module
        self.context_var_name, self.obj_id = context_var_name, obj_id
        self.var_name = var_name
        self.ordering = ordering
        self.comment_type = comment_type

    def render(self, context):
        from django.conf import settings
        if self.context_var_name is not None:
            try:
                self.obj_id = template.resolve_variable(self.context_var_name, context)
            except template.VariableDoesNotExist:
                return ''
        comment_list = Comment.objects.comments_for_object(settings.SITE_ID, self.package, self.module, self.obj_id, self.comment_type)
        comment_list = comment_list.order_by(self.ordering + 'submit_date').select_related()

        context[self.var_name] = comment_list
        return ''


@register.tag
def get_public_comment_count(parser, token):
    return _get_comment_count(parser, token, 'comment')

@register.tag
def get_public_trackback_count(parser, token):
    return _get_comment_count(parser, token, 'trackback')


def _get_comment_count(parser, token, comment_type):
    """
    Retrieves the number of comments attached to a particular object
    and stores them in a context variable.

    The difference between this tag and Django's built-in comment
    count tags is that this tag will only count comments with
    ``is_public=True``. If your application uses any sort of comment
    moderation which sets ``is_public=False``, you'll probably want to
    use this tag, as it gives an accurate count of the comments which
    will be publicly displayed.
    
    Syntax::
    
        {% get_public_comment_count for [app_name].[model_name] [object_id] as [varname] %}
    
    
    Example::

        {% get_public_comment_count for weblog.entry entry.id as comment_count %}

    """
    bits = token.contents.split()
    if len(bits) != 6:
        raise template.TemplateSyntaxError("'%s' tag takes five arguments" % bits[0])
    if bits[1] != 'for':
        raise template.TemplateSyntaxError("first argument to '%s' tag must be 'for'" % bits[0])
    try:
        app_name, model_name = bits[2].split('.')
    except ValueError:
        raise template.TemplateSyntaxError("second argument to '%s tag must be in the format app_name.model_name'" % bits[0])
    model = get_model(app_name, model_name)
    if model is None:
        raise template.TemplateSyntaxError("'%s' tag got invalid model '%s.%s'" % (bits[0], app_name, model_name))
    content_type = ContentType.objects.get_for_model(model)
    var_name, object_id = None, None
    if bits[3].isdigit():
        object_id = bits[3]
        try:
            content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            raise template.TemplateSyntaxError("'%s' tag got reference to %s object with id %s, which doesn't exist" % (bits[0], content_type.name, object_id))
    else:
        var_name = bits[3]
    if bits[4] != 'as':
        raise template.TemplateSyntaxError("fourth argument to '%s' tag must be 'as'" % bits[0])
    
    return PublicCommentCountNode(app_name, model_name, var_name, object_id, bits[5], comment_type)


class PublicCommentCountNode(template.Node):
    def __init__(self, package, module, context_var_name, obj_id, var_name, comment_type):
        self.package, self.module = package, module
        self.context_var_name, self.obj_id = context_var_name, obj_id
        self.var_name = var_name
        self.comment_type = comment_type

    def render(self, context):
        from django.conf import settings
        if self.context_var_name is not None:
            object_id = template.resolve_variable(self.context_var_name, context)
        else:
            object_id = self.obj_id
        comment_count = Comment.objects.comments_for_object(settings.SITE_ID, self.package, self.module, object_id, self.comment_type).count()
        context[self.var_name] = comment_count
        return ''
