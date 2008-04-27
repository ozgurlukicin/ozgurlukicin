#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.mail import *

def render_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)

# Copied from django's own send_mail and added header function parameter. Django's built-in send_mail() doesn't support it.
# This is used by Forum and Bug page to support threading e-mailing by adding Message-ID manually.

def send_mail_with_header(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, headers=None):
    """
    Easy wrapper for sending a single message to a recipient list. All members
    of the recipient list will see the other recipients in the 'To' field.

    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    NOTE: This method is deprecated. It exists for backwards compatibility.
    New code should use the EmailMessage class directly.
    """
    connection = SMTPConnection(username=auth_user, password=auth_password,
                                 fail_silently=fail_silently)
    return EmailMessage(subject, message, from_email, recipient_list, connection=connection, headers=headers).send()
