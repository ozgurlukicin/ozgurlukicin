#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from os import path

from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render_to_response

from oi.upload.models import Image
from oi.settings import MEDIA_URL, MEDIA_ROOT

@login_required
def image_upload(request):

    if request.user.is_staff:
        manipulator = Image.AddManipulator()
        form = forms.FormWrapper(manipulator,{},{})

        if request.POST or request.FILES:
            new_data = request.POST.copy()
            new_data.update(request.FILES)

            errors  = manipulator.get_validation_errors(new_data)
            print(errors)

            if not errors:
                if not path.exists(MEDIA_ROOT + "upload/image/" + new_data['file_file']['filename']):
                    manipulator.save(new_data)
                return render_to_response('file_upload/file_upload_success.html', {'filename': new_data['file_file']['filename']})
            else:
                return render_to_response('file_upload/file_upload.html', {'form': form, 'errors': errors})
                errors = new_data = {}
        else:
            return render_to_response('file_upload/file_upload.html', {'form': form})

    else:
        HttpResponseRedirect('/')
