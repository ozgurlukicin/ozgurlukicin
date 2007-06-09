#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime
from time import strftime, localtime

from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render_to_response

from oi.upload.models import FileUpload

@login_required
def upload(request):

    if request.user.is_staff:
        manipulator = FileUpload.AddManipulator()
        form = forms.FormWrapper(manipulator,{},{})

        if request.POST or request.FILES:
            new_data = request.POST.copy()
            new_data.update(request.FILES)

            errors = manipulator.get_validation_errors(new_data)
            if not errors:
                new_message = manipulator.save(new_data) 

            errors  = manipulator.get_validation_errors(new_data)
            print(errors)

            if not errors:
                manipulator.save(new_data)
                return render_to_response('file_upload_success.html', {'url':new_data['file_file']['filename']})
            else:
                return render_to_response('file_upload.html', {'form': form, 'errors': errors})
                errors = new_data = {}
        else:
            return render_to_response('file_upload.html', {'form': form})

    else:
        HttpResponseRedirect('/')