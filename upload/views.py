#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from os import path

from django.contrib.auth.decorators import permission_required
from django import forms
from django.shortcuts import render_to_response
from oi.upload.models import Image, ImageUploadForm
from oi.settings import MEDIA_URL, MEDIA_ROOT

@permission_required('upload.add_image', login_url="/kullanici/giris/")
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            dest = open('%s/upload/image/%s' % (MEDIA_ROOT, f.name), 'wb+')
            for chunk in f.chunks():
                dest.write(chunk)
            dest.close()
            return render_to_response('file_upload/file_upload_success.html', { 'filename': f.name})
    else:
        form = ImageUploadForm()
        return render_to_response('file_upload/file_upload.html', {'form': form})
