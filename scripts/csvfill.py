#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import locale
import sys

from django.template import Context, loader
from django.core.mail import EmailMessage

from oi.shipit.models import CdClient, Cargo, CargoCompany
from oi.settings import DEFAULT_FROM_EMAIL
from oi.shipit.settings import CD_MAIL_LIST

class InvalidEntry(Exception):pass

def parseColumn(cols):
    try:
        return cols[3].replace('"',''), cols[5].replace('"', '').split()
    except IndexError:
        raise InvalidEntry

def main():
    locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")
    errors = []
    found_clients = []
    lines = open("x.csv").readlines()[2:-1]
    company = CargoCompany.objects.all()[0]
    for line in lines:
        cols=line.split(",")
        try:
            id,name=parseColumn(cols)
            clients = CdClient.objects.filter(confirmed=True, sent=False, first_name__icontains=name[0], last_name__icontains=name[-1])
            if clients.count() != 1:
                raise InvalidEntry
            client = clients[0]
            cdClient = client

            cargo = Cargo.objects.create(cdclient=client, follow_code=str(id), company=company, date=datetime.date.today())
            message = loader.get_template("shipit/sent_email.html").render(Context({"cdClient":cdClient,"cargo":cargo}))
            mail = EmailMessage(
                "Pardus CD isteğiniz",
                message,
                "Özgürlükiçin <%s>" % DEFAULT_FROM_EMAIL,
                [CD_MAIL_LIST],
                headers={"Message-ID":"%s-%s" % (cdClient.id, cdClient.hash)}
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)

            client.sent = True
            client.save()
            found_clients.append(client)
        except InvalidEntry:
            errors.append(line)

    if errors:
        open("errors.csv",'w').writelines(errors)
    print "Total:", len(lines)
    print "Sent:", len(found_clients)
    print "Errors (written to errors.csv):", len(errors)

if __name__ == "__main__":
    main()
