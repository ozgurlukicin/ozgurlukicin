#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

def create_person(request):
    if request.method == "POST":
        form = CdClientForm(request.POST.copy())
        flood, timeout = flood_control(request)
        if form.is_valid() and not flood:
            cdClient = form.save()
            message = loader.get_template("piyango/confirm_email.html").render(Context({"cdClient":cdClient}))
            mail = EmailMessage("Pardus Çekilişi", message, "Özgürlükiçin <%s>" % DEFAULT_FROM_EMAIL, ["%s <%s>" % (cdClient.get_full_name(), cdClient.email)])
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            return render_response(request, "piyango/sent.html", locals())
    else:
        initial = {}
        if request.user.is_authenticated():
            initial["first_name"] = request.user.first_name
            initial["last_name"] = request.user.last_name
            initial["email"] = request.user.email
            initial["city"] = request.user.get_profile().city
        form = CdClientForm(initial=initial)
    return render_response(request, "piyango/create_cdclient.html", locals())

def confirm_person(request, id, hash):
    cdClient = get_object_or_404(CdClient, id=id, hash=hash, confirmed=False)
    if CdClient.objects.filter(tcidentity=cdClient.tcidentity, confirmed=True).count()>0:
        return HttpResponse("Bu TC kimlik numarası daha önce kullanılmış!")
    cdClient.confirmed = True
    cdClient.save()
    #send mail to lists
    message = loader.get_template("piyango/confirmed_email.html").render(Context({"cdClient":cdClient,"WEB_URL":WEB_URL}))
    mail = EmailMessage(
        "Pardus CD isteği",
        message,
        "Özgürlükiçin <%s>" % DEFAULT_FROM_EMAIL,
        [CD_MAIL_LIST],
        headers={"Message-ID":"%s-%s" % (cdClient.id, cdClient.hash)}
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=True)

    return render_response(request, "piyango/confirmed.html", locals())

@permission_required("piyango.change_person")
def cdclient_list(request):
    if request.method == "POST":
        form = SearchForm(request.POST.copy())
        if form.is_valid():
            term = form.cleaned_data["term"]
            cdClient_list = CdClient.objects.filter(Q(first_name__icontains=term)|Q(last_name__icontains=term)|Q(address__icontains=term)|Q(phone_number__icontains=term)).filter(sent=False, confirmed=True)
    else:
        form = SearchForm()

    return render_response(request, "piyango/person_list.html", locals())
