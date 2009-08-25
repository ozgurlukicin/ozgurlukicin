#!/usr/bin/python
# -*- coding: utf-8 -*-

# make all wallpapers antialiased

import time

import Image

from oi.tema.models import Wallpaper

for wallpaper in Wallpaper.objects.all():
    if wallpaper.papers.count() > 1:
        print "fixing", wallpaper
        biggestWallpaper = wallpaper.papers.all()[0]
        otherWallpapers = wallpaper.papers.all()[1:]

        for smallWallpaper in otherWallpapers:
            image = Image.open(biggestWallpaper.image.path)
            if image.size[0] == 1280 and image.size[1] == 1024:
                image = image.crop((0, 32, 1280, 992))

            smallImage = Image.open(smallWallpaper.image.path)
            image.thumbnail(smallImage.size, Image.ANTIALIAS)
            image.save(smallWallpaper.image.path)
            print "done", smallImage
            time.sleep(0.1)
    else:
        print "skipping", wallpaper
