#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import datetime, tempfile, os

import Image, ImageFont, ImageDraw

from oi.forum.views import flood_control
from oi.st.wrappers import render_response
from oi.tema.models import ThemeItem, File, ScreenShot, Vote, ThemeAbuseReport, DesktopScreenshot, Wallpaper, Font
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

category_dict = {
    "duvar-kagitlari": (Wallpaper, "tema/themeitem_wallpaper_detail.html"),
    "masaustu-goruntuleri": (DesktopScreenshot, "tema/themeitem_desktopscreenshot_detail.html"),
    "yazitipleri": (Font, "tema/themeitem_font_detail.html"),
}

def replace_turkish(text):
    #replace Turkish characters
    for i in TURKISH_CHARS:
        text = text.replace(i[0], i[1])
    return text

def themeitem_list(request, category=None):
    "List approved theme items"
    if category_dict.has_key(category):
        themeItems = category_dict[category][0].objects.all()
    else:
        themeItems = ThemeItem.objects.all()

    themeItems = themeItems.filter(status=True).order_by("-update")
    params = {
            "queryset": themeItems,
            "paginate_by": THEME_ITEM_PER_PAGE,
            "template_name": "tema/themeitem_list.html",
            "extra_context": {"category":category},
    }
    return object_list(request, **params)

def themeitem_detail(request, category, slug):
    #get category specific things
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
    themeItems = ThemeItem.objects.filter(status=True, author=user)

    params={
            'queryset': themeItems,
            'paginate_by': THEME_ITEM_PER_PAGE,
            "template_name": "tema/themeitem_list.html",
            "extra_context": {"author":user,"category":None},
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

def themeitem_rate(request, item_id):
    themeitem = get_object_or_404(ThemeItem, id=item_id)
    if not request.user.is_authenticated():
        return HttpResponse('Oy kullanmak için giriş yapmalısınız!')
    if request.method == "POST":
        form = ThemeRatingForm(request.POST.copy())
        if form.is_valid():
            if Vote.objects.filter(theme_item=item_id, user=request.user).count()<1:
                #create new vote
                Vote.objects.create(theme_item=themeitem, user=request.user, rating=int(float(form.cleaned_data["rating"])*20))
            else:
                #update existing vote
                vote = Vote.objects.get(theme_item=themeitem, user=request.user)
                vote.rating = int(float(form.cleaned_data["rating"])*20)
                vote.save()
            themeitem.update_rating()
    return HttpResponse("%.1f/10 (%d oy)" % (themeitem.get_rating_percent(), themeitem.vote_set.count()))

def themeitem_get_rating(request, item_id):
    themeitem = get_object_or_404(ThemeItem, id=item_id)

@login_required
def themeitem_add(request):
    if request.method == "POST":
        form = ThemeTypeForm(request.POST.copy())
        if form.is_valid():
            return HttpResponseRedirect("/tema/ekle/" + form.cleaned_data["category"])
    else:
        form = ThemeTypeForm()
    return render_response(request, "tema/themeitem_add.html", locals())

def font_image(request, slug, text):
    font = get_object_or_404(Font, slug=slug)
    #create thumbnail
    twidth = 440
    theight = 80
    image = Image.new("RGBA", (twidth, theight))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font.font.path, 50)
    fill = (112,112,112)
    draw.text((5, 5), text, font=font, fill=fill)
    #FIXME: We should get png data without writing to disk
    handle, tmp = tempfile.mkstemp(suffix=".png")
    image.save(tmp)
    data = open(tmp).read()
    os.unlink(tmp)
    return HttpResponse(data, mimetype="image/png")

@login_required
def themeitem_add_font(request):
    if request.method == "POST":
        form = FontForm(request.POST.copy(), request.FILES)
        flood, timeout = flood_control(request)

        if form.is_valid() and not flood:
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

            #create thumbnail
            twidth = 150
            theight = 100
            thumbnail = Image.new("RGBA", (twidth, theight))
            draw = ImageDraw.Draw(thumbnail)
            bigfont = ImageFont.truetype(item.font.path, 22)
            smallfont = ImageFont.truetype(item.font.path, 14)
            fill = (112,112,112)
            draw.text((5, 5), "Aa Ee Rr", font=bigfont, fill=fill)
            text_list = (
                (30, "Dag basini", u"Dağ başını"),
                (45, "duman almis,", u"duman almış,"),
                (60, "Gumus dere", u"Gümüş dere"),
                (75, "durmaz akar.", u"durmaz akar."),
            )
            for text in text_list:
                s = draw.textsize(text[1], font=smallfont)
                x = twidth - s[0] - 5
                if item.is_turkish:
                    draw.text((x, text[0]), text[2], font=smallfont, fill=fill)
                else:
                    draw.text((x, text[0]), text[1], font=smallfont, fill=fill)
            file = ContentFile("")
            item.thumbnail.save(item.font.path.replace(".ttf", ".png"), file, save=True)
            thumbnail.save(item.thumbnail.path)

            #TODO: Send e-mail to admins
            return render_response(request, "tema/themeitem_add_complete.html", locals())
    else:
        tags = [t.pk for t in Tag.objects.filter(name="yazıtipi")]
        form = FontForm(initial={"tags":tags})
    return render_response(request, "tema/themeitem_add_font.html", locals())


@login_required
def themeitem_add_desktopscreenshot(request):
    if request.method == "POST":
        form = DesktopScreenShotForm(request.POST.copy(), request.FILES)
        flood, timeout = flood_control(request)

        if form.is_valid() and not flood:
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

            #create thumbnail
            thumbnail = Image.open(item.image.path)
            thumbnail.thumbnail((150,200), Image.ANTIALIAS)
            file = ContentFile("")
            item.thumbnail.save(item.image.path, file, save=True)
            thumbnail.save(item.thumbnail.path)

            #TODO: Send e-mail to admins
            return render_response(request, "tema/themeitem_add_complete.html", locals())
    else:
        tags = [t.pk for t in Tag.objects.filter(name="masaüstü")]
        form = DesktopScreenShotForm(initial={"tags":tags})
    return render_response(request, "tema/themeitem_add_desktopscreenshot.html", locals())


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
        tags = [t.pk for t in Tag.objects.filter(name="duvar kağıdı")]
        form = WallpaperForm(initial={"tags":tags})
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


@permission_required('tema.change_themeabusereport', login_url="/kullanici/giris/")
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
    elif category == "masaustu-goruntuleri":
        object = get_object_or_404(DesktopScreenshot, id=id)
        object.download_count += 1
        object.save()
    elif category == "yazitipleri":
        object = get_object_or_404(Font, id=id)
        object.download_count += 1
        object.save()
    else:
        raise Http404
    return render_response(request, "tema/themeitem_download.html", locals())

def ghns_wallpapers(request):
    xml = loader.get_template("tema/wallpaper-providers.xml").render(Context({"SITE_URL":settings.WEB_URL}))
    return HttpResponse(xml, mimetype="text/xml")

def ghns_wallpaper(request):
    wallpapers = Wallpaper.objects.filter(status=True).order_by("-update")
    xml = loader.get_template("tema/wallpaper.xml").render(Context({"SITE_URL":settings.WEB_URL,"wallpapers":wallpapers}))
    return HttpResponse(xml, mimetype="text/xml")

def ghns_wallpaper_score(request):
    wallpapers = Wallpaper.objects.filter(status=True).order_by("-rating", "-update")
    xml = loader.get_template("tema/wallpaper.xml").render(Context({"SITE_URL":settings.WEB_URL,"wallpapers":wallpapers}))
    return HttpResponse(xml, mimetype="text/xml")

def ghns_wallpaper_downloads(request):
    wallpapers = Wallpaper.objects.filter(status=True).order_by("-download_count", "-update")
    xml = loader.get_template("tema/wallpaper.xml").render(Context({"SITE_URL":settings.WEB_URL,"wallpapers":wallpapers}))
    return HttpResponse(xml, mimetype="text/xml")

@permission_required('tema.manage_queue', login_url="/kullanici/giris/")
def themeitem_queue(request):
    queue = ThemeItem.objects.filter(status=False)
    return render_response("tema/queue.html", locals())

@permission_required("tema.manage_queue", login_url="/kullanici/giris/")
def themeitem_delete(request, item_id):
    themeItem = get_object_or_404(ThemeItem, id=item_id)
    if request.method == "POST":
        themeItem.delete()
        return HttpResponseRedirect("/tema/")
    else:
        return render_response(request, "tema/themeitem_delete.html", locals())
