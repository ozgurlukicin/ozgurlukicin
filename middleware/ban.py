#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

"""For banning unwanted users"""

from django.contrib.auth import logout

from oi.profile.models import ForbiddenUsername

class BanWare(object):
    def process_request(self, request):
        try:
            ForbiddenUsername.objects.get(name=request.user)
            logout(request)
        except:
            pass
