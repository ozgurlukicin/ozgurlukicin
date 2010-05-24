#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from os import path

from django.contrib.auth.decorators import permission_required
from django import forms
from django.shortcuts import render_to_response

from django.core.files.uploadhandler import FileUploadHandler
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError

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

#from http://www.djangosnippets.org/snippets/678/
class UploadProgressCachedHandler(FileUploadHandler):
    """
    Tracks progress for file uploads.
    The http post request must contain a header or query parameter, 'X-Progress-ID'
    which should contain a unique string to identify the upload to be tracked.
    """

    def __init__(self, request=None):
        super(UploadProgressCachedHandler, self).__init__(request)
        self.progress_id = None
        self.cache_key = None

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.content_length = content_length
        if 'X-Progress-ID' in self.request.GET :
            self.progress_id = self.request.GET['X-Progress-ID']
        elif 'X-Progress-ID' in self.request.META:
            self.progress_id = self.request.META['X-Progress-ID']
        if self.progress_id:
            self.cache_key = "%s_%s" % (self.request.META['REMOTE_ADDR'], self.progress_id )
            cache.set(self.cache_key, {
                'length': self.content_length,
                'uploaded' : 0
            })

    def new_file(self, field_name, file_name, content_type, content_length, charset=None):
        pass

    def receive_data_chunk(self, raw_data, start):
        if self.cache_key:
            data = cache.get(self.cache_key)
            data['uploaded'] += self.chunk_size
            cache.set(self.cache_key, data)
        return raw_data

    def file_complete(self, file_size):
        pass

    def upload_complete(self):
        if self.cache_key:
            cache.delete(self.cache_key)

# A view to report back on upload progress:

@permission_required('upload.add_image', login_url="/kullanici/giris/")
def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        from django.utils import simplejson
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')
