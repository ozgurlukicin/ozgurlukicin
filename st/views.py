#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import sha, datetime, random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail

from oi.st.models import FS, Game, News, Package, ScreenShot, Tag, UserProfile
from oi.flatpages.models import FlatPage
from oi.st.wrappers import render_response
from oi.st.models import RegisterForm
from oi.settings import DEFAULT_FROM_EMAIL

def home(request):
    news = News.objects.all().order_by('-date')[:4]
    return render_response(request, 'home.html', locals())

def fs_main(request):
    fs_all = FS.objects.all()
    return render_response(request, 'fs_main.html', locals())

def fs_detail(request, sef_title):
    fs = FS.objects.get(sef_title=sef_title)
    tags = fs.tags.all()
    return render_response(request, 'fs_detail.html', locals())

def fs_printable(request, sef_title):
    fs = FS.objects.get(sef_title=sef_title)
    return render_response(request, 'fs_printable.html', locals())

def game_main(request):
    game_all = Game.objects.all()
    return render_response(request, 'game_main.html', locals())

def game_detail(request, sef_title):
    game = Game.objects.get(sef_title=sef_title)
    tags = game.tags.all()
    return render_response(request, 'game_detail.html', locals())

def game_printable(request, sef_title):
    game = Game.objects.get(sef_title=sef_title)
    return render_response(request, 'game_printable.html', locals())

def news_main(request):
    news = News.objects.all().order_by('-date')[:4]
    return render_response(request, 'news_main.html', locals())

def news_detail(request, sef_title):
    news = News.objects.get(sef_title=sef_title)
    tags = news.tags.all()
    return render_response(request, 'news_detail.html', locals())

def news_printable(request, sef_title):
    news = News.objects.get(sef_title=sef_title)
    return render_response(request, 'news_printable.html', locals())

def pkg_main(request):
    packages = Package.objects.all()
    packages_by_rating = Package.objects.all().order_by('-point')[:10]
    for pkg in packages_by_rating:
        pkg.point = int(round((pkg.point+1)/2))
    return render_response(request, 'package_main.html', locals())

def pkg_detail(request, name):
    package = Package.objects.get(name=name)
    tags = package.tags.all()
    licenses = package.license.all()
    sss = package.ss.all()
    return render_response(request, 'package_detail.html', locals())

def pkg_printable(request, name):
    package = Package.objects.get(name=name)
    return render_response(request, 'package_printable.html', locals())

def tag_main(request):
    tags = Tag.objects.all()
    return render_response(request, 'tag_main.html', locals())

def tag_detail(request, tag):
    news = News.objects.filter(tags__name__contains=tag)
    packages = Package.objects.filter(tags__name__contains=tag)
    games = Game.objects.filter(tags__name__contains=tag)
    fs = FS.objects.filter(tags__name__contains=tag)
    flatpages = FlatPage.objects.filter(tags__name__contains=tag)
    return render_response(request, 'tag_detail.html', locals())

@login_required
def user_dashboard(request):
    return render_response(request, 'user/dashboard.html')

def user_profile(request, name):
    infoname = name
    try:
        info = User.objects.get(username=name)
    except:
        info = None

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
            profile.contributes_summary = form.clean_data['contributes_summary']
            profile.activation_key = activation_key
            profile.key_expires = key_expires
            profile.save()

            for number in form.clean_data['contributes']: # it's ManyToManyField's unique id
                user.get_profile().contributes.add(number)

            now = datetime.datetime.now()
            (date, hour) = now.isoformat()[:16].split("T")
            email_dict = {'date': date,
                    'hour': hour,
                    'ip': request.META['REMOTE_ADDR'],
                    'link': 'http://www.ozgurlukicin.com/user/confirm/%s' % form.clean_data['username'],
                    'key': activation_key}

            email_subject = u"Ozgurlukicin.com Kullanıcı Hesabı"
            email_body = u"""Merhaba!
%(date)s %(hour)s tarihinde %(ip)s ip adresli bilgisayardan yaptığınız Ozgurlukicin.com kullanıcı hesabınızı onaylamak için aşağıdaki linke 48 saat içerisinde tıklayıp onay anahtarınızı giriniz.

-----------------
Link: %(link)s
Anahtar: %(key)s
-----------------

Teşekkürler,
Ozgurlukicin.com"""
            email_to = form.clean_data['email']
            email_recipient = ["turkay.eren@gmail.com"]

            send_mail(email_subject, email_body % email_dict, DEFAULT_FROM_EMAIL, email_recipient, fail_silently=False)

            return render_response(request, 'user/register_done.html', {'form': form,
                                                                   'user': form.clean_data['username']})
        else:
            return render_response(request, 'user/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render_response(request, 'user/register.html', {'form': form})
