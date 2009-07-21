#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime

from oi.forum.views import flood_control
from oi.st.wrappers import render_response
from oi.tema.models import ThemeItem, File, ScreenShot, Vote, ThemeAbuseReport
from oi.tema.forms import *
from oi.tema.settings import THEME_ITEM_PER_PAGE


from oi.forum.forms import AbuseForm
from oi.forum.postmarkup import render_bbcode
from oi.forum.settings import ABUSE_MAIL_LIST
from oi.settings import WEB_URL, DEFAULT_FROM_EMAIL


from django.core.mail import send_mail
from django.template.defaultfilters import striptags
from django.views.generic.list_detail import object_list
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import formset_factory
from django.template import Context, loader
from django.conf import settings
from django.template.defaultfilters import slugify

TURKISH_CHARS = (
    ("ç", "c"),
    ("ğ", "g"),
    ("ı", "i"),
    ("ö", "o"),
    ("ş", "s"),
    ("ü", "u"),
    ("Ç", "c"),
    ("Ğ", "g"),
    ("İ", "i"),
    ("Ö", "o"),
    ("Ş", "s"),
    ("Ü", "u"),
)

def replace_turkish(text):
    #replace Turkish characters
    for i in TURKISH_CHARS:
        text = text.replace(i[0], i[1])
    return text

def themeitem_list(request, category=None):
    "List approved theme items"
    #this category is fixed for now
    category = "duvar-kagitlari"
    #first we take approved items
    themeItems = ThemeItem.objects.all()
    if category == "duvar-kagitlari":
        themeItems = Wallpaper.objects.all()
    themeItems = themeItems.filter(status=True).order_by("-update")
    """
    #filter by parent category if no subcategory is selected
    if parentcategory != "tum-kategoriler":
        parentcategory = get_object_or_404(ParentCategory, slug=parentcategory)
        themeItems = themeItems.filter(parentcategory=parentcategory)
        parentcategory = parentcategory.slug

    #filter by subcategory
    if subcategory != "tumu":
        subcategory = get_object_or_404(SubCategory, slug=subcategory)
        themeItems = themeItems.filter(category=subcategory)
        subcategory = subcategory.slug

    #order_by
    if order_by == "tarih":
        themeItems = themeItems.order_by("-edit_date")
    elif order_by == "indirilme":
        themeItems = themeItems.order_by("-download_count")
    elif order_by == "puan":
        themeItems = themeItems.order_by("-rating")
    else:# order_by == "alfabe"
        themeItems = themeItems.order_by("name")
    """
    params = {
            "queryset": themeItems,
            "paginate_by": THEME_ITEM_PER_PAGE,
            "template_name": "tema/themeitem_list.html",
    }
    """
    "extra_context": {
        "order_by": order_by,
        "parentcategory": parentcategory,
        },
    """
    return object_list(request, **params)

def themeitem_detail(request, category, slug):
    #get category specific things
    category_dict = {
        "duvar-kagitlari": (Wallpaper, "tema/themeitem_wallpaper_detail.html"),
    }
    object_type = ThemeItem
    template_name = "tema/themeitem_detail.html"
    if category_dict.has_key(category):
        object_type = category_dict[category][0]
        template_name = category_dict[category][1]

    if request.user.has_perm("tema.change_themeitem"):
        object = get_object_or_404(object_type, slug=slug)
        button_change = True
    else:
        object = get_object_or_404(object_type, slug=slug, status=True)

    return render_response(request, template_name, locals())

def list_user(request, username):
    "Theme items of a user"
    user = get_object_or_404(User, username=username)
    themeItems = user.themeitem_set.filter(approved=True)

    params={
            'queryset': themeItems,
            'paginate_by': THEME_ITEM_PER_PAGE,
            }
    return object_list(request, **params)

@login_required
def report_abuse(request, item_id):
    themeitem = get_object_or_404(ThemeItem, id=item_id)

    try:
        ThemeAbuseReport.objects.get(themeitem=item_id)
        return render_response(request, "forum/forum_error.html", {"message":"Bu ileti daha önce raporlanmış."})
    except ObjectDoesNotExist:
        if request.method == 'POST':
            form = AbuseForm(request.POST.copy())
            if form.is_valid():
                report = ThemeAbuseReport(themeitem=themeitem, submitter=request.user, reason=form.cleaned_data["reason"])
                report.save()

                email_subject = "Özgürlükİçin - Tema Şikayeti"
                email_body ="""
%(topic)s başlıklı şikayet edildi.
İletiyi görmek için buraya tıklayın: %(link)s

İletinin içeriği: (<b>%(sender)s</b> tarafından yazılmış):
%(message)s
Şikayet metni buydu (%(reporter)s tarafından şikayet edilmiş):
%(reason)s
"""
                email_dict = {
                        "topic":themeitem.title,
                        "reporter":request.user.username,
                        "link":WEB_URL + themeitem.get_absolute_url(),
                        "message":striptags(render_bbcode(themeitem.text)),
                        "reason":striptags(report.reason),
                        "sender":themeitem.author.username,
                        }
                send_mail(email_subject, email_body % email_dict, DEFAULT_FROM_EMAIL, [ABUSE_MAIL_LIST], fail_silently=True)

                return render_response(request, 'forum/forum_done.html', {
                    "message": "İleti şikayetiniz ilgililere ulaştırılmıştır. Teşekkür Ederiz.",
                    "back": themeitem.get_absolute_url()
                    })
            else:
                return render_response(request, 'tema/report.html', {"form": form, "themeitem": themeitem})
        else:
            form = AbuseForm(auto_id=True)
            return render_response(request, 'tema/report.html', {"form": form, "themeitem": themeitem})

@login_required
def vote(request, item_id, rating):
    """
    Vote a theme item.
    If user has already voted, then existing vote should be changed
    """
    themeitem = get_object_or_404(ThemeItem, pk=item_id)
    rating = int(rating) * 25

    try:
        vote = Vote.objects.get(theme_item=themeitem, user=request.user.id)
        vote.rating = rating
        vote.save()

    except ObjectDoesNotExist:
        vote = Vote(theme_item=themeitem, user=request.user)
        vote.save()

    # Update rating of the item. This can be faster but this way is more convenient
    voteCount = Vote.objects.filter(theme_item=themeitem).count()
    rating = 0
    for vote in Vote.objects.filter(theme_item=themeitem):
        rating += vote.rating
    themeitem.rating = rating / voteCount
    themeitem.save()
    return HttpResponseRedirect(themeitem.get_absolute_url())

@login_required
def themeitem_add(request):
    if request.method == "POST":
        form = ThemeTypeForm(request.POST.copy())
        if form.is_valid():
            return HttpResponseRedirect("/tema/ekle/" + form.cleaned_data["category"])
    else:
        form = ThemeTypeForm()
    return render_response(request, "tema/themeitem_add.html", locals())

@login_required
def themeitem_add_wallpaper(request):
    #TODO: add SVG support
    WallpaperFileFormSet = formset_factory(WallpaperFileForm)
    if request.method == "POST":
        form = WallpaperForm(request.POST.copy())
        fileforms = WallpaperFileFormSet(request.POST.copy(), request.FILES)
        flood, timeout = flood_control(request)

        if form.is_valid() and fileforms.is_valid() and not flood:
            item = form.save(commit=False)
            item.author = request.user
            item.submit = item.update = datetime.datetime.now()
            slug = slugify(replace_turkish(item.title))
            item.save()
            for tag in form.cleaned_data["tags"]:
                t=Tag.objects.get(name=tag)
                item.tags.add(t)
            item.slug = str(item.id) + "-" + slug
            item.save()
            for form in fileforms.forms:
                paper = form.save(commit=False)
                paper.title = "%dx%d" % (paper.image.width, paper.image.height)
                paper.save()
                item.title = item.title.replace(paper.title, "")
                item.save()
                if form.cleaned_data["create_smaller_wallpapers"]:
                    item.create_smaller_wallpapers(paper)
                item.papers.add(paper)

            #create thumbnail from first paper
            firstpaper = item.papers.all()[0]
            thumbnail = Image.open(firstpaper.image.path)
            thumbnail.thumbnail((150,200), Image.ANTIALIAS)
            file = ContentFile("")
            item.thumbnail.save(firstpaper.image.path, file, save=True)
            thumbnail.save(item.thumbnail.path)

            #TODO: Send e-mail to admins
            return render_response(request, "tema/themeitem_add_complete.html", locals())
    else:
        form = WallpaperForm()
        fileforms = WallpaperFileFormSet()
    return render_response(request, "tema/themeitem_add_wallpaper.html", locals())

@login_required
def themeitem_change(request, item_id):
    object = get_object_or_404(ThemeItem, pk=item_id)
    if request.user == object.author or request.user.has_perm("can_change_themeitem"):
        if request.method == "POST":
            form = ThemeItemForm(request.POST.copy())
            flood, timeout = flood_control(request)
            if flood:
                render_response(request, "tema/message.html", {"type": "error", "message": "Lütfen %s saniye sonra tekrar deneyiniz." % timeout })

            if form.is_valid():
                object.name = form.cleaned_data["name"]
                object.category = form.cleaned_data["category"]
                object.license = form.cleaned_data["license"]
                object.description = form.cleaned_data["description"]
                object.changelog = form.cleaned_data["changelog"]
                object.comment_enabled = form.cleaned_data["comment_enabled"]
                object.parentcategory = object.category.parent
                object.save()
                return HttpResponseRedirect(object.get_absolute_url())
            else:
                return render_response(request, "tema/themeitem_change.html", locals())
        else:
            default_data = {
                    "name": object.name,
                    "category": object.category.id,
                    "license": object.license.id,
                    "description": object.description,
                    "changelog": object.changelog,
                    "comment_enabled": object.comment_enabled,
                    }
            form = ThemeItemForm(initial=default_data)
        return render_response(request, "tema/themeitem_change.html", locals())
    else:
        return render_response(request, "tema/message.html", {"type": "error", "message": "Bu işlemi yapmak için yetkiniz yok."})


@permission_required('tema.can_change_themeabusereport', login_url="/kullanici/giris/")
def list_abuse(request):
    abuse_count = ThemeAbuseReport.objects.count()

    if request.method == 'POST':
        list = request.POST.getlist('abuse_list')
        for id in list:
            ThemeAbuseReport.objects.get(id=id).delete()
        return HttpResponseRedirect(request.path)
    else:
        if ThemeAbuseReport.objects.count() == 0:
            return render_response(request, 'tema/abuse_list.html', {'no_entry': True})
        else:
            abuse_list = ThemeAbuseReport.objects.all()
            return render_response(request, 'tema/abuse_list.html', {'abuse_list': abuse_list, "abuse_count":abuse_count})


def themeitem_download(request, category, slug, id):
    if category == "duvar-kagitlari":
        object = get_object_or_404(WallpaperFile, id=id)
        wallpaper = object.wallpaper_set.all()[0]
        wallpaper.download_count += 1
        wallpaper.save()
    else:
        raise Http404
    return render_response(request, "tema/themeitem_download.html", locals())

def ghns_wallpapers(request):
    xml = loader.get_template("tema/wallpaper-providers.xml").render(Context({"SITE_URL":settings.WEB_URL}))
    return HttpResponse(xml, mimetype="text/xml")

def ghns_wallpaper(request):
    wallpapers = Wallpaper.objects.filter(status=True).order_by("update")
    xml = loader.get_template("tema/wallpaper.xml").render(Context({"SITE_URL":settings.WEB_URL,"wallpapers":wallpapers}))
    return HttpResponse(xml, mimetype="text/xml")

def ghns_wallpaper_score(request):
    wallpapers = Wallpaper.objects.filter(status=True).order_by("rating", "update")
    xml = loader.get_template("tema/wallpaper.xml").render(Context({"SITE_URL":settings.WEB_URL,"wallpapers":wallpapers}))
    return HttpResponse(xml, mimetype="text/xml")

def ghns_wallpaper_downloads(request):
    wallpapers = Wallpaper.objects.filter(status=True).order_by("download_count", "update")
    xml = loader.get_template("tema/wallpaper.xml").render(Context({"SITE_URL":settings.WEB_URL,"wallpapers":wallpapers}))
    return HttpResponse(xml, mimetype="text/xml")

@permission_required('tema.manage_queue', login_url="/kullanici/giris/")
def themeitem_queue(request):
    queue = ThemeItem.objects.filter(status=False)
    return render_response("tema/queue.html", locals())
