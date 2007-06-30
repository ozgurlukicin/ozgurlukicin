#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import sha, datetime, random
from os import path

from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from oi.settings import DEFAULT_FROM_EMAIL, LOGIN_REDIRECT_URL, NEWS_IN_HOMEPAGE, WEB_URL, PROFILE_EDIT_URL

from oi.st.models import FS, Game, News, Package, ScreenShot, Tag, UserProfile, RegisterForm, ProfileEditForm, PardusVersion, PardusMirror, Video
from oi.st.wrappers import render_response
from oi.flatpages.models import FlatPage

def home(request):
    news = News.objects.filter(status=1).order_by('-date')[:NEWS_IN_HOMEPAGE]
    return render_response(request, 'home.html', locals())

def fs_detail(request, slug):
    fs = get_object_or_404(FS, slug=slug)
    tags = fs.tags.all()
    videos = fs.videos.all()
    return render_response(request, 'fs/fs_detail.html', locals())

def fs_printable(request, slug):
    fs = get_object_or_404(FS, slug=slug)
    return render_response(request, 'fs/fs_printable.html', locals())

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    tags = game.tags.all()
    videos = game.videos.all()
    licenses = game.license.all()
    game.avg = ((game.gameplay+game.graphics+game.sound+game.scenario+game.atmosphere)/5.0)
    return render_response(request, 'game/game_detail.html', locals())

def game_printable(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render_response(request, 'game/game_printable.html', locals())

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    tags = news.tags.all()
    return render_response(request, 'news/news_detail.html', locals())

def news_printable(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render_response(request, 'news/news_printable.html', locals())

def pkg_detail(request, name):
    package = get_object_or_404(Package, name=name)
    tags = package.tags.all()
    videos = package.videos.all()
    for video in videos:
        video.name = path.splitext(video.file)[0].split('/')[2]
    licenses = package.license.all()
    sss = package.ss.all()
    return render_response(request, 'package/package_detail.html', locals())

def pkg_printable(request, name):
    package = get_object_or_404(Package, name=name)
    return render_response(request, 'package/package_printable.html', locals())

def tag_detail(request, tag):
    try:
        news = News.objects.filter(tags__name__exact=tag)
        packages = Package.objects.filter(tags__name__exact=tag)
        games = Game.objects.filter(tags__name__exact=tag)
        fs = FS.objects.filter(tags__name__exact=tag)
        flatpages = FlatPage.objects.filter(tags__name__exact=tag)
    except Tag.DoesNotExist:
        raise Http404
    return render_response(request, 'tag/tag_detail.html', locals())

@login_required
def user_dashboard(request):
    return render_response(request, 'user/dashboard.html')

@login_required
def user_profile_edit(request):
    u = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        form.set_user(request.user)

        if form.is_valid():
            if len(form.clean_data['password']) > 0:
                u.set_password(form.clean_data['password'])

            u.first_name = form.clean_data['firstname']
            u.last_name = form.clean_data['lastname']
            u.email = form.clean_data['email']
            u.get_profile().homepage = form.clean_data['homepage']
            u.get_profile().city = form.clean_data['city']
            u.get_profile().birthday = form.clean_data['birthday']
            u.get_profile().show_email = form.clean_data['show_email']
            u.get_profile().save()
            u.save()

            return HttpResponseRedirect(PROFILE_EDIT_URL)
        else:
            return render_response(request, 'user/profile_edit.html', {'form': form})
    else:
        # convert returned value "day/month/year"
        get = str(u.get_profile().birthday)
        get = get.split("-")

        birthday = "%s/%s/%s" % (get[2], get[1], get[0])
        default_data = {'firstname': u.first_name,
                        'lastname': u.last_name,
                        'birthday': birthday,
                        'homepage': u.get_profile().homepage,
                        'city': u.get_profile().city,
                        'email': u.email,
                        'show_email': u.get_profile().show_email}

        form = ProfileEditForm(default_data)
        form.set_user(request.user)

        return render_response(request, 'user/profile_edit.html', {'form': form})

def user_profile(request, name):
    try:
        info = User.objects.get(username=name)
    except User.DoesNotExist:
        raise Http404
    return render_response(request, 'user/profile.html', locals())

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.clean_data['username'], form.clean_data['email'], form.clean_data['password'])
            user.first_name = form.clean_data['firstname']
            user.last_name = form.clean_data['lastname']
            user.is_active = False
            user.save()

            # create a key
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+form.clean_data['username']).hexdigest() # yes, i'm paranoiac
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            profile = UserProfile(user=user)
            profile.homepage = form.clean_data['homepage']
            profile.birthday = form.clean_data['birthday']
            profile.city = form.clean_data['city']
            profile.contributes_summary = form.clean_data['contributes_summary']
            profile.activation_key = activation_key
            profile.show_email = form.clean_data['show_email']
            profile.key_expires = key_expires
            profile.save()

            for number in form.clean_data['contributes']: # it's ManyToManyField's unique id
                user.get_profile().contributes.add(number)

            now = datetime.datetime.now()
            (date, hour) = now.isoformat()[:16].split("T")
            email_dict = {'date': date,
                    'hour': hour,
                    'ip': request.META['REMOTE_ADDR'],
                    'user': form.clean_data['username'],
                    'link': 'http://www.ozgurlukicin.com/confirm/%s/%s' % (form.clean_data['username'], activation_key)}

            email_subject = u"Ozgurlukicin.com Kullanıcı Hesabı, %(user)s"
            email_body = u"""Merhaba!
%(date)s %(hour)s tarihinde %(ip)s ip adresli bilgisayardan yaptığınız Ozgurlukicin.com kullanıcı hesabınızı onaylamak için aşağıdaki linke 48 saat içerisinde tıklayınız.

<a href="%(link)s">%(link)s</a>

Teşekkürler,
Ozgurlukicin.com"""
            email_to = form.clean_data['email']
            email_recipient = ["turkay.eren@gmail.com"] # this is just for testing, it should be changed when authentication system has been finished

            send_mail(email_subject, email_body % email_dict, DEFAULT_FROM_EMAIL, email_recipient, fail_silently=False)

            return render_response(request, 'user/register_done.html', {'form': form,
                                                                   'user': form.clean_data['username']})
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

def download(request):
    version = PardusVersion.objects.filter(status=1).order_by('-number')[:1][0]
    mirrors = PardusMirror.objects.filter(status=1).order_by('-name')
    return render_response(request, 'download.html', locals())

def download_detail_releasenotes(request, version):
    releasenote = get_object_or_404(PardusVersion, number=version).releasenote
    return render_response(request, 'download_relnotes.html', locals())

def videobox(request, video):
    vid = get_object_or_404(Video, file=("upload/video/%s.flv" % video))
    web_url = WEB_URL
    return render_response(request, 'videobox.html', locals())

def test(request):
    return render_response(request, 'test.html')