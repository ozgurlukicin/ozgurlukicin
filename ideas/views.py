#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from oi.forum.customgeneric import object_list
from oi.ideas.forms import *
from oi.forum.models import Post, Topic, Forum
from oi.st.wrappers import render_response
from oi.ideas.models import Idea, Category, Related, Status, Tag, Vote, Favorite
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from oi.settings import MEDIA_ROOT
from oi.ideas.settings import IDEAS_PER_PAGE
import datetime


def list(request, field="", filter_slug=""):
    ideas = Idea.objects.filter(is_hidden=False, status__is_invalid=False).order_by("-vote_count", "-id")
    if field == 'kategori':
        category_id = get_object_or_404(Category, slug = filter_slug)
        ideas = ideas.filter(category=category_id)
        page_title = "%s kategorisindeki fikirler" % category_id
    elif field == 'etiket':
        ideas = ideas.filter(tags__name__exact=filter_slug)
        page_title = "%s etiketli fikirler" % filter_slug
    elif field == 'ilgili':
        related_id = get_object_or_404(Related, name=filter_slug)
        ideas = ideas.filter(related_to=related_id)
        page_title = "%s ile ilgili fikirler" % filter_slug
    elif field == 'ekleyen':
        submitter_id = get_object_or_404(User, username=filter_slug)
        ideas = ideas.filter(submitter=submitter_id)
        page_title = "%s tarafından eklenen fikirler" % filter_slug
    elif field == 'populer':
        if filter_slug == 'bugun':
            ideas = ideas.filter(submitted_date__gt=datetime.datetime.now()-datetime.timedelta(1))
            page_title = "Bugünkü popüler fikirler"
        elif filter_slug == 'buhafta':
            ideas = ideas.filter(submitted_date__gt=datetime.datetime.now()-datetime.timedelta(7))
            page_title = "Bu haftaki popüler fikirler"
        elif filter_slug == 'buay':
            ideas = ideas.filter(submitted_date__gt=datetime.datetime.now()-datetime.timedelta(30))
            page_title = "Bu ayki popüler fikirler"
        elif filter_slug == 'tumzamanlar':
            page_title = "Tüm zamanların popüler fikirleri"
    elif field == 'son':
        if filter_slug == 'yorumlar':
            ideas = ideas.order_by("topic__topic_latest_post").filter(topic__posts__gt=1)
            page_title = "En son yorum alan iletiler"
        if filter_slug == 'eklenen':
            ideas = ideas.order_by("-submitted_date")
            page_title = "Son eklenen fikirler"
    elif field == 'durum':
        if filter_slug == "cozum-surecinde":
            s = Status.objects.get(name="Çözüm Sürecinde")
            ideas = ideas.filter(status=s)
            page_title = "Çözüme kavuşmuş fikirler"
        if filter_slug == "cozuldu":
            s = Status.objects.get(name="Çözüldü")
            ideas = ideas.filter(status=s)
            page_title = "Çözüme kavuşmuş fikirler"
        if filter_slug == "gonullu_araniyor":
            s = Status.objects.get(name="Gönüllü Aranıyor")
            ideas = ideas.filter(status=s)
            page_title = "Gönüllü arayan fikirler"
        if filter_slug == "gecersiz":
            ideas = Idea.objects.filter(is_hidden=False, status__is_invalid=True).order_by("-vote_count", "-id")
            page_title = "Geçersiz Fikirler"
    elif field == 'favori' and filter_slug == 'fikirler':
        page_title = "Favori fikirleriniz"
        try:
            favorites = Favorite.objects.filter(user=request.user.id)
            ideas = []
            i = 0
            for idea_id in favorites:
                ideas.append(favorites[i].idea)
                i += 1
        except ObjectDoesNotExist:
            pass
    else:
        page_title = "Son iki günün popüler fikirleri"
        ideas = ideas.filter(submitted_date__gt=datetime.datetime.now()-datetime.timedelta(2))
        if ideas.count() < 5:
            ideas = Idea.objects.filter(is_hidden=False, status__is_invalid=False).order_by("-submitted_date")[:5]
            page_title = "Son beş fikir"
    categories = Category.objects.order_by('name')
    if request.user.is_authenticated():
        if request.GET.has_key("page"):
            page = int(request.GET["page"])
        else:
            page = 1
        for idea in ideas[(page-1)*IDEAS_PER_PAGE:page*IDEAS_PER_PAGE]:
            try:
                f = Favorite.objects.get(user=request.user.id, idea=idea.id)
                idea.is_favorited = True
            except ObjectDoesNotExist:
                idea.is_favorited = False
            try:
                v = Vote.objects.get(user=request.user.id, idea=idea.id)
                idea.user_vote = v.vote
            except ObjectDoesNotExist:
                pass
            try:
                topic = Topic.objects.filter(title=idea.title)[0]
                idea.comment_count = topic.posts - 1
                idea.comment_url = topic.get_latest_post_url()
            except:
                idea.comment_count = 0
    return object_list(request, ideas,
            paginate_by=IDEAS_PER_PAGE,
            template_name="idea_list.html",
            extra_context={"page_title":page_title},
            )

def detail(request, idea_id):
    absolute_url = "/yenifikir"
    idea = get_object_or_404(Idea, pk=idea_id, is_hidden=False)
    user_can_change_idea = False
    if request.user.is_authenticated():
        if request.user.id == idea.submitter_id or request.user.has_perm("ideas.change_idea"):
            user_can_change_idea = True
        try:
            f = Favorite.objects.get(user=request.user, idea=idea)
            idea.is_favorited = True
        except ObjectDoesNotExist:
            idea.is_favorited = False
        try:
            v = Vote.objects.get(user=request.user.id, idea=idea.id)
            idea.user_vote = v.vote
        except ObjectDoesNotExist:
            pass

    idea.save()
    statusform = Status.objects.all()
    duplicates = Idea.objects.filter(duplicate=idea)
    duplicate_of = idea.duplicate
    bugs = idea.bug_numbers.replace(" ","").split(",")
    categories = Category.objects.order_by('name')
    page_title = "%d numaralı fikrin detayları" % idea.id
    return render_response(request, "idea_detail.html", locals())

@login_required
def add(request):
    if request.method == 'POST':
        form = NewIdeaForm(request.POST, request.FILES)
        if form.is_valid():
            forum = Forum.objects.get(name="Yeni Fikirler")
            topic = Topic(forum=forum,
                          title=form.cleaned_data['title'],
                          )
            topic.save()

            newidea = Idea(title = form.cleaned_data['title'],
                           description = form.cleaned_data['description'],
                           submitter = request.user,
                           category = form.cleaned_data['category'],
                           related_to = form.cleaned_data['related_to'],
                           forum_url = form.cleaned_data['forum_url'],
                           bug_numbers = form.cleaned_data['bug_numbers'],
                           status = Status.objects.get(name="Yeni Fikir"),
                           topic = topic)
            newidea.save()

            for tag in form.cleaned_data['tags']:
                tag = Tag.objects.get(name=tag)
                newidea.tags.add(tag)
                topic.tags.add(tag)

            post_text = "<p>#" + str(newidea.id) + " "
            post_text += "<a href=" + newidea.get_absolute_url() + ">" + newidea.title + "</a></p>"
            post_text += "<p>" + newidea.description + "</p>"
            if form.cleaned_data['forum_url']:
                post_text += "<p>İlgili Forum Linki<br /><a href='" + newidea.forum_url + "'>" + newidea.forum_url + "</a></p>"
            if newidea.bug_numbers:
                post_text += "<p>İlgili hatalar<br />"
                for bug in newidea.bug_numbers.replace(" ", "").split(","):
                    post_text += "<a href='http://bugs.pardus.org.tr/show_bug.cgi?id=" + bug + "'>" + bug + "</a> "

            post = Post(topic=topic,
                        author=request.user,
                        text=post_text)
            post.save()
            topic.topic_latest_post = post
            topic.posts = 1
            topic.save()
            topic.forum.forum_latest_post = post
            topic.forum.topics += 1
            topic.forum.posts += 1
            topic.forum.save()
            return HttpResponseRedirect(newidea.get_absolute_url())
    else:
        form = NewIdeaForm(auto_id=True)

    page_title = "Yeni Fikir Ekle"
    categories = Category.objects.all()
    return render_response(request, "idea_add_form.html", locals())

@login_required
def edit_idea(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    if request.user == idea.submitter or request.user.has_perm("ideas.change_idea"):
        if request.method == 'POST':
            form = NewIdeaForm(request.POST)
            if form.is_valid():
                idea.tags.clear()
                for tag in form.cleaned_data['tags']:
                    t = Tag.objects.get(name=tag)
                    idea.tags.add(t)

                idea.title = form.cleaned_data['title']
                idea.description = form.cleaned_data['description']
                idea.category = form.cleaned_data['category']
                idea.related_to = form.cleaned_data['related_to']
                idea.forum_url = form.cleaned_data['forum_url']
                idea.bug_numbers = form.cleaned_data['bug_numbers']
                idea.save()

                #update topic
                topic = idea.topic
                topic.tags.clear()
                for tag in idea.tags.all():
                    topic.tags.add(tag)

                topic.title = idea.title
                topic.save()

                post = topic.post_set.order_by("created")[0]
                post_text = "<p>#" + str(idea.id) + " "
                post_text += "<a href=" + idea.get_absolute_url() + ">" + idea.title + "</a></p>"
                post_text += "<p>" + idea.description + "</p>"
                if form.cleaned_data['forum_url']:
                    post_text += "<p>İlgili Forum Linki<br /><a href='" + idea.forum_url + "'>" + idea.forum_url + "</a></p>"
                if idea.bug_numbers:
                    post_text += "<p>İlgili hatalar<br />"
                    for bug in idea.bug_numbers.replace(" ", "").split(","):
                        post_text += "<a href='http://bugs.pardus.org.tr/show_bug.cgi?id=" + bug + "'>" + bug + "</a> "

                post.text = post_text
                post.save()
                return HttpResponseRedirect(idea.get_absolute_url())
            else:
                return render_response(request, "idea_add_form.html", locals())
        else:
            form_data = {
                'title': idea.title,
                'description': idea.description,
                'category': idea.category_id,
                'related_to': idea.related_to_id,
                'forum_url': idea.forum_url,
                'bug_numbers': idea.bug_numbers,
                'tags': [tag.id for tag in idea.tags.all()],
                }
            form = NewIdeaForm(form_data)
            return render_response(request, "idea_add_form.html", locals())
    else:
        """ idea isn't yours error """
        return HttpResponseRedirect(idea.get_absolute_url())

@permission_required('ideas.change_idea', login_url="/kullanici/giris/")
def delete_idea(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    idea.is_hidden = True
    idea.save()
    return HttpResponseRedirect("/yenifikir/")

@login_required
def vote(request):
    idea = request.POST.get('idea', False)
    vote = int(request.POST.get('vote', False))

    idea = get_object_or_404(Idea, pk=idea)
    evote = Vote.objects.filter(user=request.user, idea=idea)

    if evote.count() != 0:
        evote = evote[0]
        if vote != evote.vote:
            if vote == 1:
                idea.vote_count += 2
            elif vote == -1:
                idea.vote_count -= 2
            idea.save()
            evote.vote = vote
            evote.save()
    else:
        if vote == 1:
            idea.vote_count += 1
        elif vote == -1:
            idea.vote_count -= 1
        idea.save()
        evote = Vote.objects.create(user=request.user, idea=idea, vote=vote)
        evote.save()
    return HttpResponse("OK%s" % str(idea.vote_count))

@login_required
def add_favorite(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    try:
        favorite = Favorite.objects.get(user=request.user, idea=idea)
        favorited = True
    except ObjectDoesNotExist:
        favorite = Favorite(user=request.user, idea=idea)
        favorite.save()
    return HttpResponse("OK")

@login_required
def del_favorite(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    favorite = Favorite.objects.get(user=request.user, idea=idea_id)
    favorite.delete()
    return HttpResponse("OK")

@permission_required('ideas.change_idea', login_url="/kullanici/giris/")
def duplicate(request, idea_id, duplicate_id):
    try:
        idea = Idea.objects.get(pk=idea_id)
        idea_duplicate = Idea.objects.get(pk=duplicate_id)
        idea_duplicate.vote_count += idea.vote_count
        idea_duplicate.is_duplicate = True
        idea_duplicate.save()
        idea.duplicate = idea_duplicate
        idea.save()
        return HttpResponse("OK")
    except ObjectDoesNotExist:
        return HttpResponse("YOK")

@permission_required('ideas.change_idea', login_url="/kullanici/giris/")
def change_status(request, idea_id, new_status):
    idea = Idea.objects.get(pk=idea_id)
    idea.status_id = new_status
    idea.save()
    return HttpResponse("OK")
