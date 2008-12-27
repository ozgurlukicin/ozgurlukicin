#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
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
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import send_mail
from oi.st.tags import Tag
from oi.st.models import News
from oi.poll.models import Poll, PollOption, PollVote

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
                try:
                    if forum.id in request.session["read_forum_dict"] and\
                            forum.forum_latest_post.edited < request.session["read_forum_dict"][forum.id]:
                        forum.is_read = True
                    elif not forum.forum_latest_post or request.session["last_visit"] > forum.forum_latest_post.edited:
                        forum.is_read = True
                    else:
                        forum.is_read = False
                except AttributeError, ObjectDoesNotExist:
                    forum.is_read = True

    # latest topics with polls
    latest_topics_with_polls = []
    for poll in Poll.objects.order_by("-created")[:5]:
        if poll.topic_set.count() >= 1:
            latest_topics_with_polls.append(poll.topic_set.all()[0])

    usercount = User.objects.count()
    currentdate = datetime.now()
    latest_posts = Topic.objects.filter(topic_latest_post__hidden=False).order_by("topic_latest_post").distinct()[:5]
    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    return render_response(request, 'forum/forum_list.html', locals())

def forum(request, forum_slug):
    lastvisit_control(request)

    forum = get_object_or_404(Forum, slug=forum_slug)
    topics = forum.topic_set.all().order_by('-sticky', 'topic_latest_post')

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

def latest_topics(request):
    lastvisit_control(request)
    topics = Topic.objects.filter(topic_latest_post__hidden=False).order_by("topic_latest_post").distinct()[:100]

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

    forum = Forum(
            name = "Güncellenen Konular",
            slug = "guncellenen-konular",
            )

    return customgeneric.object_list(request, topics,
                       template_name = 'forum/forum_detail.html',
                       template_object_name = 'topic',
                       extra_context = {'forum': forum, 'abuse_count': abuse_count},
                       paginate_by = TOPICS_PER_PAGE,
                       allow_empty = True)

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

    # abuse reports for admins
    abuse_count = 0
    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    # create polloption percents and poll_enabled information if topic has a poll
    poll_options = poll_enabled = False
    try:
        # calculate percents
        poll = topic.poll
        poll_options = poll.polloption_set.all()
        total_vote_count = poll.pollvote_set.count() * 1.0
        for option in poll_options:
            if len(option.text) > 16:
                option.text = option.text[:16] + "..."
            if total_vote_count < 1:
                option.percent = 0
            else:
                option.percent = int(option.vote_count / total_vote_count * 100)
        # now let's see if we'll enable voting for this user
        if request.user.is_authenticated():
            if poll.date_limit:
                poll_enabled = poll.end_date > datetime.now()
            else:
                poll_enabled = True
            try:
                PollVote.objects.get(poll=poll, voter=request.user)
                # user has voted before, let's see if we'll still enable the poll
                if poll_enabled:
                    if not poll.allow_changing_vote:
                        poll_enabled = False
            except ObjectDoesNotExist:
                pass
    except: #DoesNotExist
        pass

    # If the topic is hidden and user doesn't have permission to see it, return 404.
    # If it isn't controlled, user knowing Topic URL can see it :)

    if topic.hidden and not request.user.has_perm("forum.can_see_hidden_topics"):
        return render_response(request, "404.html")

    return object_list(request, posts,
                       template_name = 'forum/topic.html',
                       template_object_name = 'post',
                       extra_context = {
                           'forum': forum,
                           'topic': topic,
                           'news_list': news_list,
                           "watching": watching,
                           "abuse_count": abuse_count,
                           "poll_options": poll_options,
                           "poll_enabled": poll_enabled,
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
    topic = get_object_or_404(Topic, pk=topic_id)

    posts = topic.post_set.order_by('-created')[:POSTS_PER_PAGE]

    if topic.forum.locked or topic.locked:
        return render_response(request, "forum/forum_error.html", {"message": "forum ya da başlık kilitli"})

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

            # send mailing list also.
            # send_mail_with_header('Re: %s' % topic.title,
            #                       '%s\n%s<br /><br /><a href="%s">%s</a>' % (css, render_bbcode(form.cleaned_data['text']), post_url, post_url),
            #                       '%s <%s>' % (request.user.username, FORUM_FROM_EMAIL),
            #                       [FORUM_MESSAGE_LIST],
            #                       headers = {'Message-ID': post.get_email_id(),
            #                                  'In-Reply-To': in_reply_to},
            #                       fail_silently = True
            #                       )

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
            topic.save()

            # add tags
            for tag in form.cleaned_data['tags']:
                t=Tag.objects.get(name=tag)
                topic.tags.add(t)

            post = Post(topic=topic,
                        author=request.user,
                        text=form.cleaned_data['text'])

            post.save()

            # generate post url
            post_url = WEB_URL + topic.get_absolute_url()

            # send e-mail to mailing list. We really rock, yeah!
            # send_mail_with_header('%s' % topic.title,
            #                       '%s<br /><br /><a href="%s">%s</a>' % (post.text, post_url, post_url),
            #                       '%s <%s>' % (request.user.username, FORUM_FROM_EMAIL),
            #                       [FORUM_MESSAGE_LIST],
            #                       headers = {'Message-ID': topic.get_email_id()},
            #                       fail_silently = True
            #                       )

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
            # Change source forum's latest post if necessary
            if forum.forum_latest_post == topic.topic_latest_post:
                # if there's no message left in source forum, clear it
                if forum.topics < 1:
                    forum.forum_latest_post = None
                else:
                    # look for new latest (It shouldn't be hidden)
                    topics = forum.topic_set.all()
                    newlatestpost = topics[0].topic_latest_post
                    for t in topics:
                        latestpost = t.topic_latest_post
                        if latestpost.edited > newlatestpost.edited:
                            newlatestpost = latestpost
                    forum.forum_latest_post = newlatestpost

                # check if this is the latest in new forum
                if forum2_object.topics > 1:
                    if forum2_object.forum_latest_post.edited < topic.topic_latest_post.edited:
                        forum2_object.forum_latest_post =  topic.topic_latest_post
                else:
                    forum2_object.forum_latest_post = topic.topic_latest_post
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

@permission_required('forum.can_create_poll', login_url="/kullanici/giris/")
def create_poll(request, forum_slug, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    forum = topic.forum
    if forum.slug != forum_slug:
        return HttpResponseRedirect(topic.get_create_poll_url())

    # check locks
    if forum.locked or topic.locked:
        return HttpResponse('Forum or topic is locked')

    # check if it already has a poll
    if topic.poll:
        return HttpResponse('Bu konuya zaten anket eklenmiş')

    if request.method == 'POST':
        form = PollForm(request.POST.copy())
        if form.is_valid():
            # create the poll
            poll = Poll(
                    question = form.cleaned_data["question"],
                    allow_changing_vote = form.cleaned_data["allow_changing_vote"],
                    allow_multiple_choices = form.cleaned_data["allow_multiple_choices"],
                    date_limit = form.cleaned_data["date_limit"],
                    end_date = form.cleaned_data["end_date"],
                    )
            poll.save()

            # create poll options
            for i in range(8):
                if form.cleaned_data["option%d" % i]:
                    option = PollOption(
                            poll = poll,
                            text = form.cleaned_data["option%d" % i],
                            )
                    option.save()

            # now add it to topic
            topic.poll = poll
            topic.save()

            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        form = PollForm()

    return render_response(request, "forum/create_poll.html", locals())

@permission_required("forum.can_change_poll", login_url="/kullanici/giris/")
def change_poll(request, forum_slug, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    forum = topic.forum
    if forum.slug != forum_slug:
        return HttpResponseRedirect(topic.get_change_poll_url())

    # check poll
    try:
        poll = topic.poll
    except: #DoesNotExist
        return HttpResponseRedirect(topic.get_create_poll_url())

    # check locks
    if forum.locked or topic.locked:
        return HttpResponse('Forum or topic is locked')

    if request.method == 'POST':
        form = PollForm(request.POST.copy())
        if form.is_valid():
            # change the poll
            poll.question = form.cleaned_data["question"]
            poll.allow_changing_vote = form.cleaned_data["allow_changing_vote"]
            poll.date_limit = form.cleaned_data["date_limit"]
            poll.end_date = form.cleaned_data["end_date"]
            poll.save()

            # change options, this is tricky
            options = poll.polloption_set.all()
            j = options.count()

            # existing options may be deleted or changed, so let's do it
            tobedeleted = []
            for i in range(j):
                if form.cleaned_data["option%d" % i]:
                    option = options[i]
                    option.text = form.cleaned_data["option%d" % i]
                    option.save()
                else:
                    tobedeleted.append(options[i])
            # now delete them
            for option in tobedeleted:
                option.delete()

            # create non-existing options
            for i in range(j, 8):
                if form.cleaned_data["option%d" % i]:
                    option = PollOption(
                            poll = poll,
                            text = form.cleaned_data["option%d" % i],
                            )
                    option.save()

            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        # convert returned value "day/month/year"
        if poll.end_date:
            end_date = poll.end_date.strftime("%d/%m/%Y")
        else:
            end_date = None
        initial = {
                "question": poll.question,
                "allow_changing_vote": poll.allow_changing_vote,
                "allow_multiple_choices": poll.allow_multiple_choices,
                "date_limit": poll.date_limit,
                "end_date": end_date,
                }

        # add options to initial data
        i = 0
        for option in poll.polloption_set.all():
            initial["option%d" % i] = option.text
            i += 1
        form = PollForm(initial=initial)

    return render_response(request, "forum/change_poll.html", locals())

@login_required
def vote_poll(request,forum_slug,topic_id,option_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    option = get_object_or_404(PollOption, pk=option_id)
    forum = topic.forum
    if forum.slug != forum_slug:
        return HttpResponseRedirect(topic.get_absolute_url())

    # check poll
    try:
        poll = topic.poll
    except: #DoesNotExist
        return HttpResponseRedirect(topic.get_absolute_url())

    # check if this option belongs to the poll
    if option.poll != poll:
        return HttpResponseRedirect(topic.get_absolute_url())

    # check locks
    if forum.locked or topic.locked:
        return HttpResponse("Forum ya da başlık kilitlidir.")

    # check date
    if poll.date_limit and datetime.now() > poll.end_date:
        return HttpResponse("Oylama süresi dolmuştur.")

    if poll.allow_multiple_choices:
        # select/unselect option
        try:
            vote = PollVote.objects.get(option=option, voter=request.user)
            if poll.allow_changing_vote:
                vote.option.vote_count = vote.option.pollvote_set.count() - 1
                vote.option.save()
                vote.delete()
        except ObjectDoesNotExist:
            vote = PollVote(
                    poll=poll,
                    option=option,
                    voter=request.user,
                    voter_ip=request.META.get('REMOTE_ADDR', None),
                    )
            vote.save()
            option.vote_count = option.pollvote_set.count()
            option.save()
    else:
        # create or change vote
        try:
            vote = PollVote.objects.get(poll=poll, voter=request.user)
            if poll.allow_changing_vote:
                vote.option.vote_count = vote.option.pollvote_set.count() - 1
                vote.option.save()
                vote.delete()
                vote = PollVote(
                        poll=poll,
                        option=option,
                        voter=request.user,
                        voter_ip=request.META.get('REMOTE_ADDR', None),
                        )
                vote.save()
                option.vote_count = option.pollvote_set.count()
                option.save()
        except ObjectDoesNotExist:
            vote = PollVote(
                    poll=poll,
                    option=option,
                    voter=request.user,
                    voter_ip=request.META.get('REMOTE_ADDR', None),
                    )
            vote.save()
            option.vote_count = option.pollvote_set.count()
            option.save()
        except MultipleObjectsReturned:
            # This is not supposed to happen, but let's take cover
            PollVote.objects.filter(poll=poll, voter=request.user)[0].delete()

    return HttpResponseRedirect(topic.get_absolute_url())

@permission_required("forum.can_change_poll", login_url="/kullanici/giris/")
def delete_poll(request, forum_slug, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    forum = topic.forum
    if forum.slug != forum_slug:
        return HttpResponseRedirect(topic.get_absolute_url())

    # check poll
    try:
        poll = topic.poll
    except: #DoesNotExist
        return HttpResponseRedirect(topic.get_absolute_url())

    # check locks
    if forum.locked or topic.locked:
        return HttpResponse('Forum or topic is locked')

    topic.poll=None
    topic.save()
    poll.delete()
    return HttpResponseRedirect(topic.get_absolute_url())
