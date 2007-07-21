#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from oi.st.models import Game, FS, News, Package
from oi.settings import WEB_URL, SITE_NAME, SITE_DESC, NEWS_IN_HOMEPAGE, PACKAGES_IN_HOMEPAGE, GAMES_IN_HOMEPAGE, FS_IN_HOMEPAGE, NEWS_PER_PAGE, PACKAGE_PER_PAGE, GAME_PER_PAGE, FS_PER_PAGE

class Main_RSS(Feed):
    title = SITE_NAME + " - Anasayfa"
    link = WEB_URL
    description = SITE_DESC
    title_template = 'feeds/feed_title.html'
    description_template = 'feeds/feed_description.html'

    def items(self):
        output = []
        for news in News.objects.order_by('-date')[:NEWS_IN_HOMEPAGE]:
            news.title = 'Haber: %s' % news.title
            output.append(news)

        for package in Package.objects.order_by('-update')[:PACKAGES_IN_HOMEPAGE]:
            package.title = 'Paket: %s' % package.title
            output.append(package)

        for game in Game.objects.order_by('-update')[:GAMES_IN_HOMEPAGE]:
            game.title = 'Oyun: %s' % game.title
            output.append(game)

        for fs in FS.objects.order_by('-update')[:FS_IN_HOMEPAGE]:
            fs.title = 'İlk Adım: %s' % fs.title
            output.append(fs)

        return output

class Main_Atom(Main_RSS):
    feed_type = Atom1Feed
    subtitle = Main_RSS.description

class News_RSS(Feed):
    title = SITE_NAME + " - Haberler"
    link = WEB_URL
    description = SITE_DESC
    title_template = 'feeds/feed_title.html'
    description_template = 'feeds/feed_description.html'

    def items(self):
        return News.objects.filter(status=1).order_by('-date')[:NEWS_PER_PAGE]

class News_Atom(News_RSS):
    feed_type = Atom1Feed
    subtitle = News_RSS.description

class FS_RSS(Feed):
    title = SITE_NAME + " - İlk Adımlar"
    link = WEB_URL
    description = SITE_DESC
    title_template = 'feeds/feed_title.html'
    description_template = 'feeds/feed_description.html'

    def items(self):
        return FS.objects.filter(status=1).order_by('-update')[:FS_PER_PAGE]

class FS_Atom(FS_RSS):
    feed_type = Atom1Feed
    subtitle = FS_RSS.description

class Game_RSS(Feed):
    title = SITE_NAME + " - Oyunlar"
    link = WEB_URL
    description = SITE_DESC
    title_template = 'feeds/feed_title.html'
    description_template = 'feeds/feed_description.html'

    def items(self):
        return Game.objects.filter(status=1).order_by('-update')[:GAME_PER_PAGE]

class Game_Atom(Game_RSS):
    feed_type = Atom1Feed
    subtitle = Game_RSS.description

class Package_RSS(Feed):
    title = SITE_NAME + " - Paketler"
    link = WEB_URL
    description = SITE_DESC
    title_template = 'feeds/feed_title.html'
    description_template = 'feeds/feed_description.html'

    def items(self):
        return Package.objects.filter(status=1).order_by('-update')[:PACKAGE_PER_PAGE]

class Package_Atom(Package_RSS):
    feed_type = Atom1Feed
    subtitle = Package_RSS.description
