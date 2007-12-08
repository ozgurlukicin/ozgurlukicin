#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from utils import remove_model_thumbnails,make_thumbnail

def crt_thumb(sender, instance, signal, *args,**kwargs):
	""" create a new thumb for the created url"""
	
	#when it is deleted control if it has a thumbnail?
	make_thumbnail(instance.file)
	

def rm_thumb(sender, instance, signal, *args,**kwargs):
	""" Delete the ones that we dont need anymore"""
	
	remove_model_thumbnails(instance)
	
