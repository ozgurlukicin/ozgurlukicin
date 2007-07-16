#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib.syndication.feeds import Feed

from oi.st.models import Game, FS, News, Package
from oi.settings import NEWS_IN_HOMEPAGE, PACKAGES_IN_HOMEPAGE, GAMES_IN_HOMAPAGE, FS_IN_HOMEPAGE

class RssMainFeed(Feed):
    title = 'Özgürlükİçin Pardus...'
    link = '/'
    description = 'Özgürlükİçin Pardus...'

    def items(self):
        output = []
        for news in News.objects.order_by('-date')[:NEWS_IN_HOMEPAGE]:
            news.title = 'Haber: %s' % news.title
            output.append(news)

        for package in Package.objects.order_by('-update')[:PACKAGES_IN_HOMEPAGE]:
            package.name = 'Paket: %s' % package.name
            output.append(package)

        for game in Game.objects.order_by('-update')[:GAMES_IN_HOMEPAGE]:
            game.title = 'Oyun: %s' % game.title
            output.append(game)

        for fs in FS.objects.order_by('-update')[:FS_IN_HOMEPAGE]:
            fs.title = 'İlk Adım: %s' % fs.title
            output.append(fs)

        return output
