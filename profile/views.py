#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import sha, datetime, random
from os import path

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from oi.settings import DEFAULT_FROM_EMAIL, LOGIN_URL, WEB_URL, PROFILE_EDIT_URL, WEB_URL

# Model object for followed topics
from oi.forum.models import WatchList, AbuseReport, Post
from oi.forum.settings import ALL_POSTS_PER_PAGE

from oi.profile.models import Avatar, Profile, LostPassword
from oi.profile.forms import RegisterForm, ProfileEditForm, LostPasswordForm, ChangePasswordForm, ResetPasswordForm
from oi.profile.settings import googleMapsApiKey
from oi.st.wrappers import render_response

@login_required
def followed_topics(request):
    if request.method == 'POST':
        list = request.POST.getlist('topic_watch_list')
        if list:
            for id in list:
                # control if posted topic id belongs to user
                if not WatchList.objects.filter(topic__id=id).filter(user__username=request.user.username):
                    return HttpResponse('Konu bu kullanıcıya ait değil!')
                else:
                    WatchList.objects.filter(topic__id=id).filter(user__username=request.user.username).delete()
        # FIXME: Shouldn't be hardcoded.
        return HttpResponseRedirect('/kullanici/takip-edilen-konular/')
    else:
        if len(WatchList.objects.filter(user__username=request.user.username)) == 0:
            return render_response(request, 'user/followed_topics.html', {'no_entry': True})
        else:
            watch_list = WatchList.objects.filter(user__username=request.user.username)
            return render_response(request, 'user/followed_topics.html', {'watch_list': watch_list})

@login_required
def posts_for_user(request, name):
    user = get_object_or_404(User, username=name)
    posts = Post.objects.filter(hidden=False, author=user).order_by('-created')
    abuse_count = 0
    if request.user.has_perm("forum.can_change_abusereport"):
        abuse_count = AbuseReport.objects.count()

    return object_list(request, posts,
            template_name = 'forum/post_list_for_user.html',
            template_object_name = 'post',
            extra_context = {'abuse_count': abuse_count, 'author': user},
            paginate_by = ALL_POSTS_PER_PAGE,
            )

@login_required
def user_dashboard(request):
    return render_response(request, 'user/dashboard.html')

@login_required
def user_profile_edit(request):
    u = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        form.set_user(u)

        if form.is_valid():
            u.first_name = form.cleaned_data['firstname']
            u.last_name = form.cleaned_data['lastname']
            u.email = form.cleaned_data['email']
            u.get_profile().homepage = form.cleaned_data['homepage']
            u.get_profile().signature = form.cleaned_data['signature']
            u.get_profile().bio = form.cleaned_data['bio']
            u.get_profile().avatar = Avatar.objects.get(file=form.cleaned_data['avatar'])
            u.get_profile().city = form.cleaned_data['city']
            u.get_profile().jabber = form.cleaned_data['jabber']
            u.get_profile().msn = form.cleaned_data['msn']
            u.get_profile().icq = form.cleaned_data['icq']
            u.get_profile().birthday = form.cleaned_data['birthday']
            u.get_profile().show_email = form.cleaned_data['show_email']
            u.get_profile().show_birthday = form.cleaned_data['show_birthday']
            u.get_profile().latitude = form.cleaned_data['latitude']
            u.get_profile().longitude = form.cleaned_data['longitude']
            u.get_profile().save()
            u.save()

            return render_response(request, 'user/profile_edit.html', {
                "profile_updated": True,
                "apikey": googleMapsApiKey,
                'form': form,
                })
        else:
            return render_response(request, 'user/profile_edit.html', {
                "form": form,
                "apikey": googleMapsApiKey,
                })
    else:
        # convert returned value "day/month/year"
        get = str(u.get_profile().birthday)
        get = get.split("-")

        birthday = "%s/%s/%s" % (get[2], get[1], get[0])
        default_data = {
                'firstname': u.first_name,
                'lastname': u.last_name,
                'avatar': u.get_profile().avatar.file,
                'birthday': birthday,
                'jabber': u.get_profile().jabber,
                'msn': u.get_profile().msn,
                'icq': u.get_profile().icq,
                'homepage': u.get_profile().homepage,
                'signature': u.get_profile().signature,
                'bio': u.get_profile().bio,
                'city': u.get_profile().city,
                'email': u.email,
                'latitude': u.get_profile().latitude,
                'longitude': u.get_profile().longitude,
                'show_email': u.get_profile().show_email,
                'show_birthday': u.get_profile().show_birthday,
                }

        form = ProfileEditForm(default_data)
        form.set_user(request.user)

        return render_response(request, 'user/profile_edit.html', {
            "form": form,
            "apikey": googleMapsApiKey,
            })

@login_required
def user_profile(request, name):
    info = get_object_or_404(User, username=name)
    has_sent_messages = info.post_set.filter(hidden=False).count() > 0
    apikey = googleMapsApiKey
    if not info.is_active:
        del info
    return render_response(request, 'user/profile.html', locals())

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.is_active = False
            user.save()

            # create a key
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+form.cleaned_data['username']).hexdigest() # yes, i'm paranoiac
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            profile = Profile(user=user)
            profile.homepage = form.cleaned_data['homepage']
            profile.birthday = form.cleaned_data['birthday']
            profile.city = form.cleaned_data['city']
            profile.contributes_summary = form.cleaned_data['contributes_summary']
            profile.activation_key = activation_key
            profile.show_email = form.cleaned_data['show_email']
            profile.key_expires = key_expires
            profile.avatar = Avatar.objects.get(id=1)
            profile.jabber = form.cleaned_data['jabber']
            profile.msn = form.cleaned_data['msn']
            profile.icq = form.cleaned_data['icq']
            profile.save()

            for number in form.cleaned_data['contributes']: # it's ManyToManyField's unique id
                user.get_profile().contributes.add(number)

            now = datetime.datetime.now()
            (date, hour) = now.isoformat()[:16].split("T")

            email_dict = {'date': date,
                    'hour': hour,
                    'ip_addr': request.META['REMOTE_ADDR'],
                    'user': user.username,
                    'link': '%s/kullanici/onay/%s/%s' % (WEB_URL, form.cleaned_data['username'], activation_key)}

            email_subject = u"Özgürlükİçin.com Kullanıcı Hesabı, %(user)s"
            email_body = u"""Merhaba!
%(date)s %(hour)s tarihinde %(ip_addr)s IP adresli bilgisayardan yaptığınız Özgurlukİçin kullanıcı hesabınızı onaylamak için lutfen asağıdaki bağlantıyı 48 saat içerisinde ziyaret ediniz.

%(link)s

Teşekkürler,
Özgurlukİçin"""

            email_to = form.cleaned_data['email']

            send_mail(email_subject % email_dict, email_body % email_dict, DEFAULT_FROM_EMAIL, [email_to], fail_silently=True)

            return render_response(request, 'user/register_done.html', {'form': form,
                                                                   'user': form.cleaned_data['username']})
        else:
            return render_response(request, 'user/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render_response(request, 'user/register.html', {'form': form})

def user_confirm(request, name, key):
    if request.user.is_authenticated():
        return render_response(request, 'user/confirm.html', {'authenticated': True})
    elif len(User.objects.filter(username=name)) == 0:
        return render_response(request, 'user/confirm.html', {'no_user': True})
    else:
        u = User.objects.get(username=name)
        if u.is_active:
            return render_response(request, 'user/confirm.html', {'actived': True})
        elif u.get_profile().activation_key == key:
            if u.get_profile().key_expires < datetime.datetime.today():
                u.delete()
                return render_response(request, 'user/confirm.html', {'key_expired': True})
            else:
                u.is_active = True
                u.save()
                return render_response(request, 'user/confirm.html', {'ok': True})
        else:
            return render_response(request, 'user/confirm.html', {'key_incorrect': True})

def lost_password(request):
    if request.method == 'POST':
       form = LostPasswordForm(request.POST)
       if form.is_valid():
           # generate new key and e-mail it to user
           salt = sha.new(str(random.random())).hexdigest()[8:]
           key = sha.new(salt).hexdigest()

           u = User.objects.get(username=form.cleaned_data['username'])
           lostpwd = LostPassword(user=u)
           lostpwd.key = key
           lostpwd.key_expires = datetime.datetime.today() + datetime.timedelta(1)
           lostpwd.save()

           now = datetime.datetime.now()
           (date, hour) = now.isoformat()[:16].split("T")

           # mail it
           email_dict = {'date': date,
                         'hour': hour,
                         'ip': request.META['REMOTE_ADDR'],
                         'user': form.cleaned_data['username'],
                         'link': 'http://www.ozgurlukicin.com/kullanici/kayip/degistir/%s' % key}

           email_subject = u"Özgürlükİçin.com Kullanıcı Parolası"
           email_body = u"""Merhaba!
%(date)s %(hour)s tarihinde %(ip)s IP adresli bilgisayardan kullanıcı parola sıfırlama isteği gönderildi. Lütfen parolanızı değiştirmek için aşağıdaki bağlantıyı 24 saat içerisinde ziyaret edin.

%(link)s"""
           email_to = form.cleaned_data['email']

           send_mail(email_subject, email_body % email_dict, DEFAULT_FROM_EMAIL, [email_to], fail_silently=True)
           return render_response(request, 'user/lostpassword_done.html')
       else:
           return render_response(request, 'user/lostpassword.html', {'form': form})
    else:
        form = LostPasswordForm()
        return render_response(request, 'user/lostpassword.html', {'form': form})

@login_required
def change_password(request):
    u = request.user
    password_changed = False

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        form.user = u

        if form.is_valid() and len(form.cleaned_data['password']) > 0:
            u.set_password(form.cleaned_data['password'])
            u.save()
            password_changed = True
    else:
        form = ChangePasswordForm()

    return render_response(request, 'user/password.html', {
        "form": form,
        "password_changed": password_changed,
        })

def reset_password(request, key):
    if LostPassword.objects.count() == 0:
        return render_response(request, 'user/change_password.html', {'error': True, 'invalid': True})

    lostpwd = LostPassword.objects.get(key=key)
    if lostpwd.is_expired():
        lostpwd.delete()
        return render_response(request, 'user/change_password.html', {'error': True, 'expired': True})
    else:
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                u = User.objects.get(username=lostpwd.user.username)
                u.set_password(form.cleaned_data['password'])
                u.save()
                lostpwd.delete()
                return render_response(request, 'user/change_password_done.html', {'login_url': LOGIN_URL})
            else:
                return render_response(request, 'user/change_password.html', {'form': form})
        else:
            form = ResetPasswordForm()
            return render_response(request, 'user/change_password.html', {'form': form})
