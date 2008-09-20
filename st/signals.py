#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 ArtIstanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

def remove_video_thumbnail_on_delete(sender, instance, signal, *args, **kwargs):
    """When video is deleted, remove it's thumbnail too"""
    from oi.settings import MEDIA_ROOT
    from os import remove

    # video filename endswith *.flv and it's thumbnail *.png. so, when we replace *.flv to *.png, we get thumbnail path
    filename = instance.file.replace('.flv', '.png')
    remove(MEDIA_ROOT + filename)
