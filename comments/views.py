'''
Copyright (c) 2006-2007, PreFab Software Inc.

Copyright (c) 2005, the Lawrence Journal-World
All rights reserved.
'''


import datetime, logging, re, time

from django import oldforms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core import validators
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required

from oi.util.fetch import read_html

from oi.comments.models import Comment
from oi.comments.templatetags.comment_honeypot import makeFieldNames, makeSpinner


COMMENTS_PER_PAGE = 20

# Minimum and maximum time allowed for comment posting, in seconds
MIN_COMMENT_TIME = 5
MAX_COMMENT_TIME = 2*60*60

class PublicCommentManipulator(oldforms.Manipulator):
    "Manipulator that handles public free (unregistered) comments"
    def __init__(self):
        self.fields = (
            oldforms.TextField(field_name="person_name", maxlength=50, is_required=True,
                validator_list=[self.hasNoProfanities]),
            oldforms.LargeTextField(field_name="comment", maxlength=3000, is_required=True,
                validator_list=[self.hasNoProfanities]),
        )

    def hasNoProfanities(self, field_data, all_data):
        if settings.COMMENTS_ALLOW_PROFANITIES:
            return
        return validators.hasNoProfanities(field_data, all_data)

    def get_comment(self, new_data):
        "Helper function"
        return Comment(content_type=ContentType.objects.get(pk=new_data["content_type_id"]),
            object_id=new_data["object_id"], comment=new_data["comment"].strip(),
            person_name=new_data["person_name"].strip(), person_email=new_data["person_email"].strip(),
            person_www=new_data["person_www"].strip(),
            submit_date=datetime.datetime.now(), is_public=new_data["is_public"],
            ip_address=new_data["ip_address"], site=Site.objects.get(id=settings.SITE_ID),
            comment_type='comment')

    def save(self, new_data):
        today = datetime.date.today()
        c = self.get_comment(new_data)
        # Check that this comment isn't duplicate. (Sometimes people post
        # comments twice by mistake.) If it is, fail silently by pretending
        # the comment was posted successfully.
        for old_comment in Comment.objects.filter(content_type__id__exact=new_data["content_type_id"],
            object_id__exact=new_data["object_id"], person_name__exact=new_data["person_name"],
            submit_date__year=today.year, submit_date__month=today.month,
            submit_date__day=today.day):
            if old_comment.comment == c.comment:
                return old_comment
        c.save()
        return c


class SpamComment(Exception): pass

@login_required
def post_comment(request):
    ''' This is a rewrite of django.contrib.comments.views.comments.post_free_comment
        implementing the honeypot ideas from
        http://www.nedbatchelder.com/text/stopbots.html

        If you want to try it out, you can use the Firefox Web Developer plugin
        to disable CSS on the comment page. That will show the honeypot fields and buttons.
        Filling in any of the honeypots or submitting with the "I'm a spambot" button
        will cause the posting to be ignored.

        The field names are all obfuscated with md5 hashes.
        The hashes include the IP address of the poster, the ID of the entry being commented on,
        and a timestamp, so they will be different each time the form is used.

        The form is timestamped. Any submission that takes less than MIN_COMMENT_TIME seconds
        or more than MAX_COMMENT_TIME seconds will be ignored.
        Any attempt to change the timestamp will be detected.

        The IP address that requested the form must match the IP address that posts the comment.
        This is checked by the spinner and can be disabled with a flag in comment_honeypot.py.
        See comments there for why you might want to do this.

        If any of the tests fail, the browser is redirected to the same page
        as it would go to with a successful post. This is a little different than
        what would normally happen if the preview button is pressed but I think it's ok.
        I didn't put up an error because I want it to look to the spambot as if it succeeded.

        Failures are logged to the logging system.
    '''

    try:
        if not request.POST:
            raise SpamComment, "GET request in comment submission"

        spinner = request.POST['spinner']   # Key used to hash field names
        fieldMap = makeFieldNames(spinner)  # Map from cleartext name to hashed name

        # Validate the spinner. This checks that the timestamp hasn't been tampered
        # and the IP address is the same as the original request
        target = request.POST[fieldMap['target']]
        content_type_id, object_id = target.split(':') # target is something like '52:5157'
        timestamp = request.POST[fieldMap['timestamp']]
        if spinner != makeSpinner(timestamp, request.META['REMOTE_ADDR'], target):
            raise SpamComment, "Invalid spinner in comment submission"

        # Check time-to-post, must be greater than MIN_COMMENT_TIME and less than MAX_COMMENT_TIME
        timeToPost = int(time.time()) - int(timestamp)
        if timeToPost < MIN_COMMENT_TIME:
            raise SpamComment, 'Comment posted too fast: %s seconds' % timeToPost
        elif timeToPost > MAX_COMMENT_TIME:
            raise SpamComment, 'Comment posted too slow: %s minutes' % (timeToPost / 60)

        if request.POST.has_key(fieldMap['submit']):
            raise SpamComment, 'User clicked Spambot button in comment submission'

        # Check the honeypot fields. If any of these are filled in, the request is
        # bogus and we redirect directly to the 'posted' page
        honeypots = 'honeypot1 honeypot2 honeypot3 honeypot4'.split()
        for honey in honeypots:
            if request.POST.get(fieldMap[honey]):
                raise SpamComment, 'User supplied honeypot field "%s" in comment submission' % honey

        content_type = ContentType.objects.get(pk=content_type_id)
        try:
            obj = content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            raise Http404, "The comment form had an invalid 'target' parameter -- the object ID was invalid"

        new_data = request.POST.copy()
        for name, scrambled in fieldMap.items():
            if request.POST.has_key(scrambled):
                new_data[name] = request.POST[scrambled]

        new_data['content_type_id'] = content_type_id
        new_data['object_id'] = object_id
        new_data['ip_address'] = request.META['REMOTE_ADDR']
        new_data['is_public'] = True
        new_data['person_email'] = request.POST[fieldMap['person_email']]
        new_data['person_www'] = request.POST[fieldMap['person_www']]

        manipulator = PublicCommentManipulator()
        errors = manipulator.get_validation_errors(new_data)
        if errors or request.POST.has_key(fieldMap['preview']):
            comment = errors and '' or manipulator.get_comment(new_data)
            return render_to_response('comments/comment_preview.html', {
                'comment': comment,
                'comment_form': oldforms.FormWrapper(manipulator, new_data, errors),
                'target': target,
                'fields': fieldMap,
                'spinner': spinner,
                'timestamp': timestamp,
                'previewText': 'Preview modified comment'

            }, context_instance=RequestContext(request))
        elif request.POST.has_key(fieldMap['post']):
            # If the IP is banned, mail the admins, do NOT save the comment, and
            # serve up the "Thanks for posting" page as if the comment WAS posted.
            if request.META['REMOTE_ADDR'] in settings.BANNED_IPS:
                from django.core.mail import mail_admins
                mail_admins("Practical joker", str(request.POST) + "\n\n" + str(request.META))
            else:
                manipulator.do_html2python(new_data)
                comment = manipulator.save(new_data)
            return HttpResponseRedirect("../posted/?c=%s:%s" % (content_type_id, object_id))
        else:
            raise Http404, "The comment form didn't provide either 'preview' or 'post'"

    except SpamComment, e:
        logging.info('Spam attempt from %s: %s' % (request.META['REMOTE_ADDR'], e))
    except MultiValueDictKeyError, e:
        key = re.search("Key '(.*?)' not found", str(e)).group(1) # The key we were looking up

        # Get the unobfuscated key name if possible
        try:
            if key in fieldMap.values():
                key = [ k for k,v in fieldMap.items() if key==v ][0]
        except NameError:   # no fieldMap
            pass
        logging.info('Missing field in comment form: %s' % key)

    # This is shared exception handling, the only way to get here is after an exception
    try:
        # If we have a target, act like a successful post
        return HttpResponseRedirect("../posted/?c=%s" % (target))
    except NameError:
        raise Http404


@login_required
def comment_was_posted(request):
    """
    Display "comment was posted" success page

    Templates: `comment_posted`
    Context:
        object
            The object the comment was posted on
    """
    obj = None
    if request.GET.has_key('c'):
        content_type_id, object_id = request.GET['c'].split(':')
        try:
            content_type = ContentType.objects.get(pk=content_type_id)
            obj = content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            pass
    return render_to_response('home.html', {'object': obj}, context_instance=RequestContext(request))


# Common trackback spam that somehow gets past the validation
_ignores = [
    '''I couldn't understand some parts of this article, but it sounds interesting'''
]

@login_required
def trackback(request, content_type_id, obj_id, entry_url):
    ''' Generic trackback handler
        @param request: Django request
        @param content_type_id: ID of the class being trackbacked
        @param obj_id: ID of the specific object being trackbacked
        @param entry_url: The URL of the original item, used to validate the trackback URL
    '''
    if not request.POST:
        # Redirect to the trackback section of the original post
        return HttpResponseRedirect(entry_url+'#trackbacks')

    url = request.POST.get('url')
    if not url:
        return trackbackError('Missing URL')

    title = request.POST.get('title', '')
    excerpt = request.POST.get('excerpt', '')
    blog_name = request.POST.get('blog_name', '')

    if not validateTrackback(url, entry_url):
        return trackbackError('This appears to be spam')

    for ignore in _ignores:
        if ignore in excerpt:
            # Pretent we liked it...
            return trackbackOk()

    content_type = ContentType.objects.get(pk=content_type_id)

    site = Site.objects.get(id=settings.SITE_ID)
    comment = Comment(content_type=content_type, object_id=obj_id, comment=excerpt,
        ip_address=request.META['REMOTE_ADDR'], site=site,
        trackback_title=title, trackback_www=url, trackback_name=blog_name,
        is_public=True, comment_type='trackback')
    comment.save()

    return trackbackOk()

@login_required
def validateTrackback(client_url, target_url):
    ''' Verify that the target URL actually appears in the page referenced by the client URL. '''
    try:
        f, data = read_html(client_url)
        if target_url in data:
            return True
    except:
        pass

    return False


def trackbackError(msg):
    content = '''<?xml version="1.0" encoding="utf-8"?>
<response>
<error>1</error>
<message>%s</message>
</response>''' % msg
    return HttpResponse(content, mimetype="text/xml; charset=utf-8")


def trackbackOk():
    content = '''<?xml version="1.0" encoding="utf-8"?>
<response>
<error>0</error>
</response>'''
    return HttpResponse(content, mimetype="text/xml; charset=utf-8")
