#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import striptags
from django.views.generic.list_detail import object_list

from oi.forum.settings import *
from oi.forum.forms import *

from oi.st.wrappers import render_response
from oi.forum.models import Category, Forum, Topic, Post, AbuseReport, WatchList
from oi.forum import customgeneric

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from oi.st.models import Tag, News

# import our function for sending e-mails and setting
from oi.st.wrappers import send_mail_with_header
from oi.settings import WEB_URL, DEFAULT_FROM_EMAIL
# import bbcode renderer for quotation
from oi.forum.postmarkup import render_bbcode

def main(request):
    lastvisit_control(request)

    categories = Category.objects.order_by('order')
    categories = [(category, category.forum_set.all()) for category in categories]
    forums = topics = posts = 0
    for category in categories:
        for forum in category[1]:
            forums += 1
            topics += forum.topics
            posts += forum.posts

            # read/unread stuff
            if request.user.is_authenticated():
                if forum.id in request.session["read_forum_dict"] and\
                        forum.forum_latest_post.edited < request.session["read_forum_dict"][forum.id]:
                    forum.is_read = True
                elif not forum.forum_latest_post or request.session["last_visit"] > forum.forum_latest_post.edited:
                    forum.is_read = True
                else:
                    forum.is_read = False

    usercount = User.objects.count()
    currentdate = datetime.now()
    latest_posts = Post.objects.filter(hidden=False).order_by("-created")[:5]
    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    return render_response(request, 'forum/forum_list.html', locals())

def forum(request, forum_slug):
    lastvisit_control(request)

    forum = get_object_or_404(Forum, slug=forum_slug)
    topics = forum.topic_set.all().order_by('-sticky', '-topic_latest_post')

    if request.user.is_authenticated():
        for topic in topics:
            if topic.topic_latest_post.edited > request.session['last_visit'] and\
                    not topic.id in request.session["read_topic_dict"]:
                topic.is_read = False
            elif topic.topic_latest_post.edited < request.session['last_visit'] or\
                    not topic.id in request.session["read_topic_dict"] or\
                    request.session["read_topic_dict"][topic.id] > topic.topic_latest_post.edited:
                topic.is_read = True
            else:
                topic.is_read = False
    abuse_count = 0
    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    return customgeneric.object_list(request, topics,
                       template_name = 'forum/forum_detail.html',
                       template_object_name = 'topic',
                       extra_context = {'forum': forum, 'abuse_count': abuse_count},
                       paginate_by = TOPICS_PER_PAGE,
                       allow_empty = True)

def latest_posts(request):
    posts = Post.objects.filter(hidden=False).order_by('-created')[:100]
    abuse_count = 0
    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    return object_list(request, posts,
            template_name = 'forum/post_list.html',
            template_object_name = 'post',
            extra_context = {'abuse_count': abuse_count},
            paginate_by = ALL_POSTS_PER_PAGE,
            )

@login_required
def unread_topics(request):
    lastvisit_control(request)

    topics = Topic.objects.order_by("-sticky", "-topic_latest_post")
    unread_topics = []
    for topic in topics:
        if topic.topic_latest_post.edited > request.session['last_visit'] and\
            not topic.id in request.session["read_topic_dict"]:
            unread_topics.append(topic)
        elif topic.topic_latest_post.edited < request.session['last_visit'] or\
            not topic.id in request.session["read_topic_dict"] or\
            request.session["read_topic_dict"][topic.id] > topic.topic_latest_post.edited:
            pass
        else:
            unread_topics.append(topic)
        if len(unread_topics) >= TOPICS_PER_PAGE:
            break
    topic_count = len(unread_topics)
    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    return render_response(request, "forum/unread.html", locals())

@login_required
def mark_all_as_read(request):
    lastvisit_control(request)

    request.session["last_visit"] = datetime.now()
    request.session["read_topic_dict"] = {}
    request.session["read_forum_dict"] = {}
    return HttpResponseRedirect(request.GET["next"])

def topic(request, forum_slug, topic_id):
    lastvisit_control(request)

    topic = get_object_or_404(Topic, pk=topic_id)
    forum = topic.forum
    if forum.slug != forum_slug:
        return HttpResponseRedirect(topic.get_absolute_url())
    posts = topic.post_set.all().order_by('created')
    news_list = News.objects.filter(status=1).order_by('-update')[:3]
    watching = False

    if request.user.is_authenticated():
        request.session["read_topic_dict"][topic.id] = datetime.now()
        request.session["read_forum_dict"][forum.id] = datetime.now()
        request.session.modified = True

        # is the user watching this topic?
        try:
            request.user.watchlist_set.get(topic__id=topic_id)
            watching = True
        except ObjectDoesNotExist:
            pass

    topic.views += 1
    topic.save()

    # we love Django, just 1 line and pagination is ready :)
    abuse_count = 0
    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    return object_list(request, posts,
                       template_name = 'forum/topic.html',
                       template_object_name = 'post',
                       extra_context = {
                           'forum': forum,
                           'topic': topic,
                           'news_list': news_list,
                           "watching": watching,
                           "abuse_count": abuse_count,
                           },
                       paginate_by = POSTS_PER_PAGE,
                       allow_empty = True)

@login_required
def follow(request, forum_slug, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    # determine if user already added this to prevent double adding.
    if len(WatchList.objects.filter(topic__id=topic_id).filter(user__username=request.user.username)) > 0:
        errorMessage = 'Bu başlığı zaten izlemektesiniz.'
        return render_response(request, 'forum/forum_error.html', {'message': errorMessage})
    else:
        watchlist = WatchList(topic=topic, user=request.user)
        watchlist.save()
        return HttpResponseRedirect(topic.get_absolute_url())

@login_required
def reply(request, forum_slug, topic_id, quote_id=False):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    posts = topic.post_set.order_by('-created')[:POSTS_PER_PAGE]

    if forum.locked or topic.locked:
        return HttpResponse("Forum or topic is locked") #FIXME: Give an error message

    if request.method == 'POST':
        form = PostForm(request.POST.copy())

        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            post = Post(topic=topic,
                        author=request.user,
                        text=form.cleaned_data['text']
                       )
            post.save()

            # generate post url
            post_url = WEB_URL + post.get_absolute_url()
            # generate In-Reply-To header. If we get quote that should be quote's message id
            if request.POST.has_key('quote_id'):
                quote = get_object_or_404(Post, id=request.POST['quote_id'])
                in_reply_to = quote.get_email_id()
            else:
                in_reply_to = topic.get_email_id()

            # sorry, we have to send <style> to be able to display quotation correctly. Hardcode for now and I know, It's really UGLY!
            # FIXME: Give postmarkup.py's QuoteTag e-mail rendering support

            css = """<style type="text/css">
.quote {
    border: 1px solid #CCCCCC;
    padding: 10px;
    margin-bottom: 8px;
    background-color: #E1E3FF;
    color: #51615D;
}

.quote p {
    padding-left: 12px;
    font-style: italic;
}
</style>"""

            # send email to everyone who follows this topic.
            watchlists = WatchList.objects.filter(topic__id=topic_id)
            for watchlist in watchlists:
                send_mail_with_header('[Ozgurlukicin-forum] Re: %s' % topic.title,
                                      '%s\n%s<br /><br /><a href="%s">%s</a>' % (css, render_bbcode(form.cleaned_data['text']), post_url, post_url),
                                      '%s <%s>' % (request.user.username, FORUM_FROM_EMAIL),
                                      [watchlist.user.email],
                                      headers = {'Message-ID': post.get_email_id(),
                                                 'In-Reply-To': in_reply_to},
                                      fail_silently = True
                                      )

            email_list = []
            # send emails to me, at least I'm the only one who are willing to follow the forum via email :)
            for user in User.objects.filter(is_staff=1):
                if user.username == 'Eren':
                    email_list.append(user.email)# send mailing list also.

            send_mail_with_header('[Ozgurlukicin-forum] Re: %s' % topic.title,
                                  '%s\n%s<br /><br /><a href="%s">%s</a>' % (css, render_bbcode(form.cleaned_data['text']), post_url, post_url),
                                  '%s <%s>' % (request.user.username, FORUM_FROM_EMAIL),
                                  email_list,
                                  headers = {'Message-ID': post.get_email_id(),
                                             'In-Reply-To': in_reply_to},
                                  fail_silently = True
                                  )

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        if quote_id:
            post = get_object_or_404(Post, pk=quote_id)

            if post in topic.post_set.all():
                form = PostForm(auto_id=True, initial={'text': '[quote <b>%s</b>, %s tarihinde:]%s[/quote]' % (post.author, post.edited.strftime("%d/%m/%Y %H:%M"), post.text)})
            # if quote doesn't belong to this topic, just redirect to what user gets :)
            else:
                return HttpResponseRedirect(post.get_absolute_url())
        else:
            form = PostForm(auto_id=True)

    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    return render_response(request, 'forum/reply.html', locals())

@login_required
def edit_post(request, forum_slug, topic_id, post_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    post = get_object_or_404(Post, pk=post_id)
    posts = topic.post_set.filter(created__lt = post.created).order_by('-created')[:POSTS_PER_PAGE]

    #the normal users dont have that permission actually
    if not request.user.has_perm('forum.change_post'):
        user=get_object_or_404(User, username=request.user.username)
        post_user=user.post_set.filter(id=post_id)

        if not post_user:
            return HttpResponse("That is a Wrong way my friend :) ")

    if forum.locked or topic.locked:
        # FIXME: Give an error message
        return HttpResponse("Forum or topic is locked")

    if request.method == 'POST':
        form = PostForm(request.POST.copy())

        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            post.text = form.cleaned_data['text']
            post.edit_count += 1
            post.edited = datetime.now()
            post.last_edited_by = request.user
            post.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        if post in topic.post_set.all():
            form = PostForm(auto_id=True, initial={'text': post.text})

    abuse_count = 0
    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    return render_response(request, 'forum/post_edit.html', locals())

@login_required
def new_topic(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug)

    if forum.locked:
        return HttpResponse('Forum is locked')

    if request.method == 'POST':
        form = TopicForm(request.POST.copy())
        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            topic = Topic(forum=forum,
                          title=form.cleaned_data['title'])
        #tags
            topic.save()

            for tag in form.cleaned_data['tags']:
                t=Tag.objects.get(name=tag)
                topic.tags.add(t)

            post = Post(topic=topic,
                        author=request.user,
                        text=form.cleaned_data['text'])

            post.save()

            # generate post url
            post_url = WEB_URL + topic.get_absolute_url()

            email_list = []
            # send emails to me, at least I'm the only one who are willing to follow the forum via email :)
            for user in User.objects.filter(is_staff=1):
                if user.username == 'Eren':
                    email_list.append(user.email)

            # send e-mail to mailing list. We really rock, yeah!
            send_mail_with_header('[Ozgurlukicin-forum] %s' % topic.title,
                                  '%s<br /><br /><a href="%s">%s</a>' % (post.text, post_url, post_url),
                                  '%s <%s>' % (request.user.username, FORUM_FROM_EMAIL),
                                  email_list,
                                  headers = {'Message-ID': topic.get_email_id()},
                                  fail_silently = True
                                  )

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = TopicForm(auto_id=True)

    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    return render_response(request, 'forum/new_topic.html', locals())

@permission_required('forum.change_topic', login_url="/kullanici/giris/")
def edit_topic(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    first_post = topic.post_set.order_by('created')[0]

    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    if forum.locked or topic.locked:
        return HttpResponse('Forum or topic is locked')

    if request.method == 'POST':
        form = TopicForm(request.POST.copy())
        flood,timeout = flood_control(request)

        if form.is_valid() and not flood:
            topic.title = form.cleaned_data['title']
            #I don't know the purpose of this so commenting out:
            #topic.topic_latest_post = first_post
            #delete tags and add new ones
            topic.tags.clear()
            for tag in form.cleaned_data['tags']:
                t=Tag.objects.get(name=tag)
                topic.tags.add(t)

            topic.save()

            first_post.edit_count += 1
            first_post.edited = datetime.now()
            first_post.last_edited_by = request.user
            first_post.save()

            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        form = TopicForm(auto_id=True, initial={
            "title": topic.title,
            "text": first_post.text,
            "tags": [tag.name for tag in topic.tags.all()],
            })

    return render_response(request, 'forum/new_topic.html', locals())

@permission_required('forum.can_merge_topic', login_url="/kullanici/giris/")
def merge(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if forum.locked or topic.locked:
        hata="Kilitli konularda bu tür işlemler yapılamaz!"
        return render_response(request, 'forum/merge.html', locals())

    if request.method == 'POST':
        form = MergeForm(request.POST.copy())

        if form.is_valid():
            topic2 = form.cleaned_data['topic2']

            if int(topic2)==topic.id:
                hata="Aynı konuyu mu merge edeceksiniz !"
                return render_response(request, 'forum/merge.html', locals())


            topic2_object=get_object_or_404(Topic, pk=int(topic2))

            posts_tomove=Post.objects.filter(topic=topic.id)
            for post in posts_tomove:
                post.topic = topic2_object
                post.save()

            #increase count
            topic2_object.posts += posts_tomove.count()
            #increase and decrease post counts in case of a merge to a different forum
            forum = topic.forum
            forum2 = topic2_object.forum
            forum.posts -= posts_tomove.count()
            forum.topics -= 1
            forum2.posts += posts_tomove.count()

            #TODO: Handle changing lastpost of a forum
            #save and delete
            forum.save()
            forum2.save()
            topic2_object.save()
            topic.delete()

            return HttpResponseRedirect(topic2_object.get_absolute_url())
        else:
            hata="Forum valid degil!"
            return render_response(request, 'forum/merge.html', locals())

    else:
        form = MergeForm(auto_id=True)

    return render_response(request, 'forum/merge.html', locals())

@permission_required('forum.can_move_topic', login_url="/kullanici/giris/")
def move(request, forum_slug, topic_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)

    if forum.locked or topic.locked:
        hata="Kilitli konularda bu tür işlemler yapılamaz!"
        return render_response(request, 'forum/move.html', locals())

    if request.method == 'POST':
        form = MoveForm(request.POST.copy())

        if form.is_valid():
            # Here is the moving thing
            forum2 = form.cleaned_data['forum2']

            if int(forum2) == forum.id:
                error = "Konu zaten bu forumda olduğu için taşınamaz!"
                return render_response(request, 'forum/move.html', locals())

            forum2_object=get_object_or_404(Forum, pk=int(forum2))
            # Change Forum
            topic.forum = forum2_object
            # Reduce post count of forum
            forum.topics -= 1
            forum.posts -= topic.posts
            forum2_object.topics += 1
            forum2_object.posts += topic.posts
            #TODO: Check if target forum has some topics or not
            # Change forum's latest post if necessary
            if forum.forum_latest_post == topic.topic_latest_post:
                # look for new latest (It shouldn't be hidden)
                topics = forum.topic_set.all()
                posts = []
                for t in topics:
                    lastpost = t.post_set.filter(hidden=False).order_by("-created")[0]
                    posts.append((lastpost.created, lastpost.id))

                newlatestpost = posts[0]
                for post in posts:
                    if post[0] > newlatestpost[0]:
                        newlatestpost = post
                newlatestpost = Post.objects.get(id=newlatestpost[1])
                # check if this is the latest in new forum
                if forum2_object.forum_latest_post.created < newlatestpost.created:
                    forum2_object.forum_latest_post = newlatestpost
            # save them
            topic.save()
            forum.save()
            forum2_object.save()
            #TODO: Inform topic author

            return HttpResponseRedirect(topic.get_absolute_url())
        else:
            error = "Forum geçerli değil!"
            return render_response(request, 'forum/move.html', locals())
    else:
        #TODO: Leave link in old forum
        form = MoveForm(auto_id=True)
        return render_response(request, 'forum/move.html', locals())

@permission_required('forum.can_hide_post', login_url="/kullanici/giris/")
def hide(request, forum_slug, topic_id, post_id=False):
    topic = get_object_or_404(Topic, pk=topic_id)

    if post_id:
        post = get_object_or_404(Post, pk=post_id)

        if post.topic.hidden:
            return render_response(request, "forum/forum_error.html", { "message":"Konu gizli olduğu için mesajı gösteremezsiniz." })
        if post.hidden:
            post.hidden = 0
        else:
            post.hidden = 1

        post.save()

        return HttpResponseRedirect(topic.get_absolute_url())
    else:
        if topic.hidden:
            topic.hidden = 0
            # we also want to hide the posts
            for post in topic.post_set.all():
                post.hidden = 0
                post.save()
        else:
            topic.hidden = 1
            for post in topic.post_set.all():
                post.hidden = 1
                post.save()

        topic.save()

        return HttpResponseRedirect(topic.forum.get_absolute_url())

@permission_required('forum.can_stick_topic', login_url="/kullanici/giris/")
def stick(request, forum_slug, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if topic.sticky:
        topic.sticky = 0
        topic.save()

        return HttpResponseRedirect(topic.forum.get_absolute_url())
    else:
        topic.sticky = 1
        topic.save()

        return HttpResponseRedirect(topic.forum.get_absolute_url())

@permission_required('forum.can_lock_topic', login_url="/kullanici/giris/")
def lock(request, forum_slug, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if topic.locked:
        topic.locked = 0
        topic.save()

        return HttpResponseRedirect(topic.forum.get_absolute_url())
    else:
        topic.locked = 1
        topic.save()

        return HttpResponseRedirect(topic.forum.get_absolute_url())

def flood_control(request):
    if 'flood_control' in request.session and ((datetime.now() - request.session['flood_control']).seconds < FLOOD_TIMEOUT):
        flood = True
        timeout = (FLOOD_TIMEOUT - (datetime.now() - request.session['flood_control']).seconds)
    elif not 'flood_control' in request.session or ((datetime.now() - request.session['flood_control']).seconds > FLOOD_TIMEOUT):
        flood = timeout = False
        request.session['flood_control'] = datetime.now()
    else:
        flood = timeout = False

    return flood,timeout

def lastvisit_control(request):
    if request.user.is_authenticated():
        if not "last_visit" in request.session:
            request.session["oi_version"] = 1141
            request.session["last_visit"] = datetime.now()
        if not "read_topic_dict" in request.session:
            request.session["read_topic_dict"] = {}
        if not "read_forum_dict" in request.session:
            request.session["read_forum_dict"] = {}

@login_required
def delete_post(request,forum_slug,topic_id, post_id):
    """ The delete part should be controlled better !"""
    forum = get_object_or_404(Forum, slug=forum_slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    post = get_object_or_404(Post, pk=post_id)

    if not request.user.has_perm('forum.delete_post'):
        #that one is wrong of course it can return more than one query ...
        #post_user=get_object_or_404(Post,author =request.user)
        user=get_object_or_404(User, username=request.user.username)
        post_user=user.post_set.filter(id=post_id)

        if not post_user:
            return HttpResponse("That is a Wrong way my friend :) ")

    if forum.locked or topic.locked:
        return HttpResponse("Forum or topic is locked")

    if request.method == 'POST':
        post.delete()

    return HttpResponseRedirect(topic.get_absolute_url())

@login_required
def report_abuse(request,post_id):
    post = get_object_or_404(Post, pk=post_id, hidden=False)
    if post.topic.locked:
        return render_response(request, "forum/forum_error.html", {"message":"Bu konu kilitlenmiş olduğu için raporlanamaz."})

    try:
        AbuseReport.objects.get(post=post_id)
        return render_response(request, "forum/forum_error.html", {"message":"Bu ileti daha önce raporlanmış."})
    except ObjectDoesNotExist:
        if request.method == 'POST':
            form = AbuseForm(request.POST.copy())
            if form.is_valid():
                report = AbuseReport(post=post, submitter=request.user, reason=form.cleaned_data["reason"])
                report.save()
                # now send mail to staff
                email_subject = "Özgürlükİçin Forum - İleti Şikayeti"
                email_body ="""
%(topic)s başlıklı konudaki bir ileti şikayet edildi.
İletiyi forumda görmek için buraya tıklayın: %(link)s

İletinin içeriği buydu (%(sender)s tarafından yazılmış):
%(message)s
Şikayet metni buydu (%(reporter)s tarafından şikayet edilmiş):
%(reason)s
"""
                email_dict = {
                        "topic":post.topic.title,
                        "reporter":request.user.username,
                        "link":WEB_URL + post.get_absolute_url(),
                        "message":striptags(render_bbcode(post.text)),
                        "reason":striptags(report.reason),
                        "sender":post.author.username,
                        }
                send_mail(email_subject, email_body % email_dict, DEFAULT_FROM_EMAIL, [ABUSE_MAIL_LIST], fail_silently=True)
                return render_response(request, 'forum/forum_done.html', {
                    "message": "İleti şikayetiniz ilgililere ulaştırılmıştır. Teşekkür Ederiz.",
                    "back": post.get_absolute_url()
                    })
        else:
            form = AbuseForm(auto_id=True)

        return render_response(request, "forum/report.html", locals())

@permission_required('forum.can_change_abusereport', login_url="/kullanici/giris/")
def list_abuse(request):
    abuse_count = AbuseReport.objects.count()

    if request.method == 'POST':
        list = request.POST.getlist('abuse_list')
        for id in list:
            AbuseReport.objects.get(id=id).delete()
        return HttpResponseRedirect(request.path)
    else:
        if AbuseReport.objects.count() == 0:
            return render_response(request, 'forum/abuse_list.html', {'no_entry': True})
        else:
            abuse_list = AbuseReport.objects.all()
            return render_response(request, 'forum/abuse_list.html', {'abuse_list': abuse_list, "abuse_count":abuse_count})
