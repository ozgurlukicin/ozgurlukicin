#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import sha, datetime, random
from os import path

from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from oi.settings import DEFAULT_FROM_EMAIL, LOGIN_URL, WEB_URL, PROFILE_EDIT_URL

from oi.profile.models import Avatar, Profile, LostPassword
from oi.profile.forms import RegisterForm, ProfileEditForm, LostPasswordForm, ChangePasswordForm, ResetPasswordForm
from oi.st.wrappers import render_response
from oi.petition.models import Petitioner

@login_required
def user_dashboard(request):
    return render_response(request, 'user/dashboard.html')

@login_required
def user_profile_edit(request):
    numberofpetitioners = Petitioner.objects.filter(is_active=True).count()
    petitionpercent = numberofpetitioners / 30
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
            u.get_profile().avatar = Avatar.objects.get(id=form.cleaned_data['avatar'])
            u.get_profile().city = form.cleaned_data['city']
            u.get_profile().jabber = form.cleaned_data['jabber']
            u.get_profile().msn = form.cleaned_data['msn']
            u.get_profile().icq = form.cleaned_data['icq']
            u.get_profile().birthday = form.cleaned_data['birthday']
            u.get_profile().show_email = form.cleaned_data['show_email']
            u.get_profile().save()
            u.save()

            return render_response(request, 'user/profile_edit.html', {
                'profile_updated': True,
                "numberofpetitioners": numberofpetitioners,
                "petitionpercent": petitionpercent,
                'form': form,
                })
        else:
            return render_response(request, 'user/profile_edit.html', {
                'form': form,
                "numberofpetitioners": numberofpetitioners,
                "petitionpercent": petitionpercent,
                })
    else:
        # convert returned value "day/month/year"
        get = str(u.get_profile().birthday)
        get = get.split("-")

        birthday = "%s/%s/%s" % (get[2], get[1], get[0])
        default_data = {'firstname': u.first_name,
                        'lastname': u.last_name,
                        'avatar': u.get_profile().avatar.id,
                        'birthday': birthday,
                        'jabber': u.get_profile().jabber,
                        'msn': u.get_profile().msn,
                        'icq': u.get_profile().icq,
                        'homepage': u.get_profile().homepage,
                        'signature': u.get_profile().signature,
                        'city': u.get_profile().city,
                        'email': u.email,
                        'show_email': u.get_profile().show_email}

        form = ProfileEditForm(default_data)
        form.set_user(request.user)

        return render_response(request, 'user/profile_edit.html', {
            "form": form,
            "numberofpetitioners": numberofpetitioners,
            "petitionpercent": petitionpercent,
            })

@login_required
def user_profile(request, name):
    info = get_object_or_404(User, username=name)
    numberofpetitioners = Petitioner.objects.filter(is_active=True).count()
    petitionpercent = numberofpetitioners / 30
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
                    'link': 'http://www.ozgurlukicin.com/kullanici/onay/%s/%s' % (form.cleaned_data['username'], activation_key)}

            email_subject = u"Ozgurlukicin.com Kullanıcı Hesabı, %(user)s"
            email_body = u"""Merhaba!
%(date)s %(hour)s tarihinde %(ip_addr)s ip adresli bilgisayardan yaptiginiz Ozgurlukicin.com kullanici hesabinizi onaylamak icin lutfen asagidaki baglantiyi 48 saat icerisinde ziyaret ediniz.

%(link)s

Tesekkurler,
Ozgurlukicin.com"""

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

           email_subject = u"Ozgurlukicin.com Kullanıcı Parolası"
           email_body = u"""Merhaba!
%(date)s %(hour)s tarihinde %(ip)s ip adresli bilgisayardan kullanici parola sifirlama istegi gonderildi. Lutfen parolanizi degistirmek icin asagidaki baglantiyi 24 saat icerisinde ziyaret edin.

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
    numberofpetitioners = Petitioner.objects.filter(is_active=True).count()
    petitionpercent = numberofpetitioners / 30
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
        "numberofpetitioners": numberofpetitioners,
        "petitionpercent": petitionpercent,
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
