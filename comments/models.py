''' 
Copyright (c) 2006-2007, PreFab Software Inc.

Copyright (c) 2005, the Lawrence Journal-World
All rights reserved.
'''


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

class CommentManager(models.Manager):
    def comments_for_object(self, site_id, app_label, model, obj_id, comment_type='comment'):
        ''' Get a QuerySet of all public comments for the specified object. '''
        kwargs = {
            'site__id__exact': site_id,
            'content_type__app_label__exact': app_label,
            'content_type__model__exact': model,
            'object_id__exact': obj_id,
            'comment_type__exact': comment_type,
            'is_public__exact': True,
        }
        return self.filter(**kwargs)
        
        
class Comment(models.Model):
    ''' Data model for both comments and trackbacks '''
    objects = CommentManager()
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(_('object ID'))
    comment = models.TextField(_('comment'), maxlength=3000)
    submit_date = models.DateTimeField(_('date/time submitted'), auto_now_add=True)
    is_public = models.BooleanField(_('is public'))
    ip_address = models.IPAddressField(_('ip address'))

    site = models.ForeignKey(Site)
    
    typeChoices = (
        ('comment', 'Comment'),
        ('trackback', 'Trackback'),
    )
    comment_type = models.CharField(maxlength=10, blank=False, choices=typeChoices, default='comment')
    
    # These fields are used only for comments
    person_name = models.CharField(_("person's name"), maxlength=50, blank=True)
    person_email = models.EmailField(_('e-mail address'), blank=True)
    person_www = models.URLField("person's URL", verify_exists=False, blank=True)
    
    # These fields are used only for trackbacks
    trackback_name = models.CharField(_("blog name"), maxlength=255, blank=True)
    trackback_title = models.CharField(_('blog entry'), maxlength=255, blank=True)
    trackback_www = models.URLField('entry URL', verify_exists=False, blank=True)
    
    
    class Meta:
        ordering = ('-submit_date',)
        
    class Admin:
        fields = (
            (None, {'fields': (('content_type', 'object_id', 'site'), 'comment', 'is_public',)}),
            ('Comment from', {'fields': ('person_name', 'person_email', 'person_www')}),
            ('Trackback from', {'fields': ('trackback_name', 'trackback_title', 'trackback_www')}),
            ('Meta', {'fields': ('submit_date', 'ip_address', 'comment_type')}),
        )
        list_display = ('person_name', 'trackback_title', 'linkToItem', 'submit_date', 'content_type', 'get_content_object', 'is_public')
        list_display_links = ('person_name', 'trackback_title')
        list_filter = ('submit_date', 'comment_type')
        date_hierarchy = 'submit_date'
        search_fields = ('comment', 'person_name', 'trackback_title', 'trackback_name')

    def __repr__(self):
        return "%s: %s..." % (self.person_name, self.comment[:100])

    def get_absolute_url(self):
        return self.get_content_object().get_absolute_url() + "#c" + str(self.id)

    def linkToItem(self):
        ''' A link to the corresponding content object's admin interface
        '''
        content = self.get_content_object()
        if not content:
            return '&nbsp;'
        
        contentUrl = "/admin/%s/%s/%s/" % (self.content_type.app_label, self.content_type.model, self.object_id)
        return '<a href="%s">%s</a>' % (contentUrl, content)
        

    # Configure linkToItem for the Admin app
    linkToItem.short_description = 'comment for'
    linkToItem.allow_tags = True
    
    
    def get_content_object(self):
        """
        Returns the object that this comment is a comment on. Returns None if
        the object no longer exists.
        """
        from django.core.exceptions import ObjectDoesNotExist
        try:
            return self.content_type.get_object_for_this_type(pk=self.object_id)
        except ObjectDoesNotExist:
            return None

    get_content_object.short_description = _('Content object')
