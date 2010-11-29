#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.list_detail import object_list
from django.core.mail import send_mail

from oi.st.wrappers import render_response
from oi.forum.views import flood_control
from oi.bug.models import Bug, Comment
from oi.bug.forms import BugForm, FullBugForm, CommentForm
from oi.bug.settings import BUGS_PER_PAGE
from oi.settings import DEBUG

try:
    BUG_USER = User.objects.get(username="akin")
except User.DoesNotExist:
    if DEBUG:
        BUG_USER = User.objects.filter(is_superuser=True)[0]
    else:
        raise

BUG_MAILLIST = BUG_USER.email
BUG_FROM_EMAIL = "hata@ozgurlukicin.com"

@login_required
def add_bug(request):
    if request.method == "POST":
        form = BugForm(request.POST.copy())
        flood, timeout = flood_control(request)

        if form.is_valid() and not flood:
            bug = Bug(
                title = form.cleaned_data["title"],
                submitter = request.user,
                description = form.cleaned_data["description"],
                priority = form.cleaned_data["priority"],
                assigned_to = BUG_USER,
                )
            bug.save()
            email_dict = {
                    "bugId": bug.id,
                    "bugTitle": bug.title,
                    "link": bug.get_full_url(),
                    "title": bug.title,
                    "priority": bug.get_priority_display(),
                    "submitter": "%s %s <%s>" % (bug.submitter.first_name, bug.submitter.last_name, bug.submitter.email),
                    "assigned_to": "%s %s <%s>" % (bug.assigned_to.first_name, bug.assigned_to.last_name, bug.assigned_to.email),
                    "description": bug.description,
                    }
            email_subject = u"[Hata %(bugId)s] Yeni: %(bugTitle)s"
            email_body = u"""%(link)s
Başlık: %(title)s
Öncelik: %(priority)s
Bildiren: %(submitter)s
Atanan: %(assigned_to)s

%(description)s
"""
            mail_set = set()
            mail_set.add(BUG_MAILLIST)
            mail_set.add(bug.submitter.email)
            mail_set.add(bug.assigned_to.email)
            # send mails seperately
            for subscriber in mail_set:
                send_mail(email_subject % email_dict, email_body % email_dict, BUG_FROM_EMAIL, [subscriber], fail_silently=True)
            return HttpResponseRedirect(bug.get_absolute_url())
    else:
        form = BugForm(auto_id=True)

    return render_response(request, 'bug/bug_add.html', locals())

@permission_required('bug.change_bug', login_url="/kullanici/giris/")
def change_bug(request, id):
    bug = Bug.objects.get(id=id)
    if request.method == "POST":
        form = FullBugForm(request.POST.copy())
        if form.is_valid():
            bug.title = form.cleaned_data["title"]
            bug.description = form.cleaned_data["description"]
            bug.priority = form.cleaned_data["priority"]
            bug.status = form.cleaned_data["status"]
            bug.assigned_to = form.cleaned_data["assigned_to"]
            bug.save()
            email_dict = {
                    "bugId": bug.id,
                    "bugTitle": bug.title,
                    "link": bug.get_full_url(),
                    "title": bug.title,
                    "priority": bug.get_priority_display(),
                    "status": bug.get_status_display(),
                    "submitter": "%s %s <%s>" % (bug.submitter.first_name, bug.submitter.last_name, bug.submitter.email),
                    "assigned_to": "%s %s <%s>" % (bug.assigned_to.first_name, bug.assigned_to.last_name, bug.assigned_to.email),
                    "description": bug.description,
                    }
            email_subject = u"[Hata %(bugId)s] %(bugTitle)s"
            email_body = u"""%(link)s
Hatada değişiklik yapıldı

Başlık: %(title)s
Öncelik: %(priority)s
Durum: %(status)s
Bildiren: %(submitter)s
Atanan: %(assigned_to)s

%(description)s
"""
            mail_set = set()
            mail_set.add(BUG_MAILLIST)
            mail_set.add(bug.submitter.email)
            mail_set.add(bug.assigned_to.email)
            comments = bug.comment_set.all()
            for comment in comments:
                mail_set.add(comment.author.email)
            # send mails seperately
            for subscriber in mail_set:
                send_mail(email_subject % email_dict, email_body % email_dict, BUG_FROM_EMAIL, [subscriber], fail_silently=True)
    return HttpResponseRedirect(bug.get_absolute_url())

@permission_required('bug.delete_bug', login_url="/kullanici/giris/")
def delete_bug(request, id):
    bug = Bug.objects.get(id=id)
    if request.method == "POST":
        bug.delete()
        return HttpResponseRedirect("/hata/")
    return render_response(request, 'bug/bug_delete_confirm.html', locals())

def main(request):
    bugs = Bug.objects.order_by("status")
    return object_list(request, bugs,
            template_name = "bug/bug_main.html",
            template_object_name = "bug",
            paginate_by = BUGS_PER_PAGE,
            allow_empty = True,
            )

def detail(request, id):
    bug = Bug.objects.get(id=id)
    default_data = {
            "title": bug.title,
            "assigned_to": bug.assigned_to.id,
            "description": bug.description,
            "status": bug.status,
            "priority": bug.priority,
            }
    bugform = FullBugForm(default_data)
    if request.method == "POST" and request.user.is_authenticated():
        form = CommentForm(request.POST.copy())
        flood, timeout = flood_control(request)

        if form.is_valid() and not flood:
            comment = Comment(
                bug = bug,
                author = request.user,
                text = form.cleaned_data["text"],
                )
            comment.save()
            comments = bug.comment_set.all()
            email_dict = {
                    "bugId": bug.id,
                    "bugTitle": bug.title,
                    "link": bug.get_full_url(),
                    "comment_count": comments.count(),
                    "author": "%s %s <%s>" % (comment.author.first_name, comment.author.last_name, comment.author.email),
                    "date": comment.date,
                    "comment": comment.text,
                    }
            email_subject = u"[Hata %(bugId)s] %(bugTitle)s"
            email_body = u"""%(link)s

-- Yorum #%(comment_count)s yazan %(author)s %(date)s --

%(comment)s
"""
            mail_set = set()
            mail_set.add(BUG_MAILLIST)
            mail_set.add(bug.submitter.email)
            mail_set.add(bug.assigned_to.email)
            for comment in comments:
                mail_set.add(comment.author.email)
            # send mails seperately
            for subscriber in mail_set:
                send_mail(email_subject % email_dict, email_body % email_dict, BUG_FROM_EMAIL, [subscriber], fail_silently=True)
    else:
        form = CommentForm()
    return render_response(request, 'bug/bug_detail.html', locals())
