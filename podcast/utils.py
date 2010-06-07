#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

def getDuration(path):
    import mad

    mf = mad.MadFile(path)
    ms = mf.total_time()
    sec = ms / 1000
    min = sec / 60
    sec %= 60

    return (min, sec)

