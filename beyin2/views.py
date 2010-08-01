#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.http import HttpResponse, HttpResponseRedirect
from oi.beyin2.models import Idea, Status, Category, Vote, Favorite, ScreenShot
from oi.beyin2.forms import IdeaForm, IdeaDuplicateForm, ScreenShotForm, TagsForm
from oi.st.wrappers import render_response
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from oi.forum.models import Topic, Forum, Post
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator
from oi.st.tags import Tag
from datetime import datetime, timedelta

DefaultCategory = 1
DefaultStatus = 1
idea_per_page = 10
# if it doesnot exist ??
ForumCategory = "Yeni Fikirler"

def main(request, idea_id = -1, page_number = 1, order = "date", filter_by = "none", filter = "none" ):
    order_dict = {
        'date': '-dateSubmitted',
        'vote_value': '-vote_value',
        'title': 'title',
        'vote_count': 'vote_count',
        'neg_date': 'dateSubmitted',
        'neg_vote_value': 'vote_value',
        'neg_title': '-title',
        'neg_vote_count': '-vote_count'}

    if request.POST:
        idea = get_object_or_404(Idea, pk = idea_id)
        try:
            idea.status = get_object_or_404(Status, name = request.POST['status'])
        except:
            idea.status = Status()
        try:
            idea.category = get_object_or_404(Category, name = request.POST['category'])
        except:
            idea.category = Category()

        idea.save()
        return HttpResponseRedirect(reverse('oi.beyin2.views.main'))
    else:
        #idea list order changes
        all_idea_list = Idea.objects.filter(is_hidden=False).order_by(order_dict[order])
        #idea list filter changes
        if filter_by == "user":
            all_idea_list = Idea.objects.filter(is_hidden = False, submitter = filter ).order_by(order_dict[order])
        if filter_by == "tag":
            tag = Tag.objects.get(name=filter)
            all_idea_list = tag.idea_set.filter(is_hidden=False).order_by(order_dict[order])
        if filter_by == "favorite":
            favorites = Favorite.objects.filter( user = request.user )
            try: 
                favorites[0]
                all_idea_list = []
                for favorite in favorites:
                    all_idea_list.append(favorite.idea)
            except:
                return render_response(request,'beyin2/idea_errorpage.html',{'error':'İsteğe uygun fikir bulunamadı.',})
        if filter_by == "today":
            all_idea_list = Idea.objects.filter( is_hidden = False, dateSubmitted__gt = datetime.now() - timedelta(1)).order_by(order_dict[order])
        if filter_by == "this_week":
            all_idea_list = Idea.objects.filter( is_hidden = False, dateSubmitted__gt = datetime.now() - timedelta(7)).order_by(order_dict[order])
        if filter_by == "this_month":
            all_idea_list = Idea.objects.filter( is_hidden = False, dateSubmitted__gt = datetime.now() - timedelta(10)).order_by(order_dict[order])
        if filter_by == "category":
            all_idea_list = Idea.objects.filter( is_hidden = False, category = filter ).order_by(order_dict[order])
        if filter_by == "status":
            all_idea_list = Idea.objects.filter( is_hidden = False, status = filter ).order_by(order_dict[order])
        if filter_by == "deleted":
            all_idea_list = Idea.objects.filter( is_hidden = True, is_duplicate = False ).order_by(order_dict[order])
        if filter_by == "duplicate":
            all_idea_list = Idea.objects.filter( is_duplicate = True ).order_by(order_dict[order])
        # add vote_counts for every vote, intended to use in preview on votebar
        for idea in all_idea_list:
            pos_votes = Vote.objects.filter( vote = 'U', idea = idea).count()
            notr_votes = Vote.objects.filter( vote = 'N', idea = idea ).count()
            neg_votes = Vote.objects.filter( vote = 'D', idea = idea ).count()
            idea.vote_text =  "Arti:%s kararsiz:%s Eksi:%s" %(pos_votes, notr_votes, neg_votes )
        status_list = Status.objects.all().order_by("name")
        category_list = Category.objects.all().order_by("name")
        if not all_idea_list:
            return render_response(request,'beyin2/idea_errorpage.html',{'error':'İsteğe uygun fikir bulunamadı.',})
        paginator = Paginator(all_idea_list, idea_per_page)
        idea_list=paginator.page(page_number)
        last_page = len(paginator.page_range)
        if int(page_number) < last_page - 4:
            show_go_to_last = True
        else:
            show_go_to_last = False
        if int(page_number) > 5:
            show_go_to_first = True
        else:
            show_go_to_first = False
        if int(page_number) > 4:
            page_range = paginator.page_range[int(page_number)-5:(int(page_number)+4)]
        else:
            page_range = paginator.page_range[0:(int(page_number)+4)]
        #we dont want to show default category, so we sould send the name to check if it is
        def_cate = get_object_or_404(Status, pk = DefaultCategory )
        for idea in idea_list.object_list:
            idea.duplicate_list = Idea.objects.filter( duplicate = idea )
        return render_response(request,'beyin2/idea_list.html',{'idea_list': idea_list, 'status_list':status_list, 'category_list': category_list,'order':order,'come_from':'main', 'page_range': page_range, 'show_go_to_last': show_go_to_last, 'show_go_to_first': show_go_to_first, 'last_page': last_page, 'default_category' : def_cate,'filter':filter,'filter_by':filter_by})

def idea_detail(request,idea_id):
    idea = get_object_or_404(Idea, pk = idea_id)
    if idea.is_hidden:
        return render_response(request,'beyin2/idea_errorpage.html',{'error':'Fikir bulunamadı',})
    status_list = Status.objects.all()
    category_list = Category.objects.all()
    def_cate = get_object_or_404(Status, pk = DefaultCategory )
    idea.duplicate_list = Idea.objects.filter( duplicate = idea )
    return render_response(request,'beyin2/idea_detail.html',{'idea': idea, 'status_list':status_list, 'category_list': category_list,'come_from':'detail', 'default_category' : def_cate})

@login_required
def vote(request, idea_id, vote ,come_from):
    if vote == "1":
        vote_choice = "U"
    elif vote == "0":
        vote_choice = "N"
    elif vote == "2":
        vote_choice = "D"
    voter = request.user
    idea = get_object_or_404(Idea, pk = idea_id)
    working_vote = Vote.objects.filter( voter=voter, idea=idea )
    if working_vote.count() !=0:
        working_vote = working_vote[0]

        # if already voted choice removed from template, this control can also removed
        if vote_choice != working_vote.vote:
            #remove the old vote
            if working_vote.vote == "U":
                idea.vote_value -=9
            elif working_vote.vote == "D":
                idea.vote_value +=11
            else:
                idea.vote_value -=1
            # add new votes value
            if vote_choice == "U":
                idea.vote_value +=9
            elif vote_choice == "D":
                idea.vote_value -=11
            else:
                idea.vote_value +=1
        else:
            return HttpResponse("you have already voted, dont cheat!")
    else:
            if vote_choice == "U":
                idea.vote_value +=9
            elif vote_choice == "D":
                idea.vote_value -=11
            else:
                idea.vote_value +=1
            #and for every vote add 1
            idea.vote_value +=1
            working_vote = Vote.objects.create( voter=voter, idea=idea, vote=vote_choice )
    working_vote.vote = vote_choice
    working_vote.save()
    all_votes = Vote.objects.filter( idea=idea ).count()
    all_votes = float(all_votes)
    u_votes = Vote.objects.filter( idea=idea, vote="U").count()
    n_votes = Vote.objects.filter( idea=idea, vote="N").count()
    d_votes = Vote.objects.filter( idea=idea, vote="D").count()
    u_percent = int((u_votes/all_votes)*100)
    n_percent = int((n_votes/all_votes)*100)
    d_percent = int((d_votes/all_votes)*100)
    percent = (u_percent*1000000)+(n_percent*1000)+d_percent
    idea.vote_percent=percent
    idea.save()
    if come_from == "detail":
        return HttpResponseRedirect(reverse('oi.beyin2.views.idea_detail', args=(idea_id,)))
    if come_from == "js_oyla":
        return HttpResponse( "%s_%s" %(idea.vote_value, idea.vote_percent))
        """if idea.vote_value > 0:
            idea_calc= idea.vote_value*1000000000+idea.vote_percent
        else:
            idea_calc = idea.vote_value*-1000000000+idea.vote_percent
            idea_calc += 1000000000000000
        return HttpResponse( str(idea_calc))"""
    return HttpResponseRedirect(reverse('oi.beyin2.views.main'))

@login_required
def select_tags(request):
    form = TagsForm()
    if request.POST:
        form = TagsForm(request.POST)
        if form.is_valid:
            dummy_idea = form.save(commit = False)

            tags = form.cleaned_data['tags']

            idea_list = Idea.objects.all()

            similars_dict = {}

            if idea_list:
                for idea in idea_list:
                    if idea.is_hidden == False and idea.is_duplicate == False:
                        idea_tag_list = idea.tags.all()
                        counter = 0
                        for tag in tags:
                            if tag in idea_tag_list:
                                counter = counter + 1

                        for i in range(0, tags.count()):
                            if tags.count() - counter == i:
                                value = '<a href="' + reverse('idea_detail', args =( idea.id,)) + '">' + idea.title
                                if idea.category:
                                    value += ' | ' + str(idea.vote_value / 10) + ' Puan' + ' | ' + idea.category.name + '</a>'
                                else:
                                    value += ' | ' + str(idea.vote_value / 10) + ' Puan' + ' | ' + 'Kategori belirtilmemiş' + '</a>'
                                value += '<br />' + idea.description[:140] + '...' + '<br /><br />'
                                similars_dict[str(i) + " " + value] = value
            else:
                return HttpResponse("IdeaYok")

            if similars_dict:
                output = ""
                liste = sorted(similars_dict.keys())
                for k in liste[:10]:
                    output += similars_dict[k]
                return HttpResponse(output)
            else:
                return HttpResponse("EslesmeYok")
        else:
            form = TagsForm()
            return render_response(request, 'beyin2/select_tags.html', {'form': form})
    return render_response(request, 'beyin2/select_tags.html', {'form': form})

@login_required
def add_new(request,phase ):
    if phase == "1":
        ScreenShotSet = formset_factory(ScreenShotForm, extra=3, max_num=3)
        ScreenShotFormSet = ScreenShotSet(prefix = 'imageform')
        form = TagsForm(request.POST)
        dummy_idea = form.save(commit = False)
        tags = form.cleaned_data['tags']
        title = form.cleaned_data['title']
        form = IdeaForm({'ideaform-title': title, 'ideaform-tags': [tag.id for tag in tags]}, prefix = 'ideaform')
        return render_response(request, 'beyin2/idea_new.html', {'form':form,'ScreenShotFormSet':ScreenShotFormSet})
    if phase == "2":
        form = IdeaForm({'title': '', 'description': '', 'status': DefaultStatus, 'category': DefaultCategory}, prefix = 'ideaform')
        ScreenShotSet = formset_factory(ScreenShotForm, extra=3, max_num=3) 
        if request.POST:
            try:
                form = IdeaForm(request.POST, prefix = 'ideaform')
                ScreenShotFormSet  = ScreenShotSet(request.POST, request.FILES, prefix = 'imageform') 
            except:
                return render_response(request,'beyin2/idea_errorpage.html',{'error':'Form bulunamadı.',})

            
            if form.is_valid():
                forum = Forum.objects.get(name = ForumCategory)
                topic = Topic(forum = forum,title = form.cleaned_data['title'])
                topic.save()

                idea = form.save(commit = False)
                idea.submitter = request.user
                idea.description = form.cleaned_data['description']
                idea.dateSubmitted = datetime.now()
                idea.topic = topic
                if not idea.status:
                    def_stat = get_object_or_404(Status, pk = DefaultStatus )
                    idea.status = def_stat
                if not idea.category:
                    def_cate = get_object_or_404(Category, pk = DefaultCategory )
                    idea.category = def_cate
                idea.save()

                try:
                    for screenshotform in ScreenShotFormSet.forms:
                        image = screenshotform.save(commit = False)
                        if image.image:
                            image.idea = idea
                            image.save()
                except:
                    pass

                for tag in form.cleaned_data['tags']:
                    tag = Tag.objects.get(name=tag)
                    idea.tags.add(tag)
                    topic.tags.add(tag)

                post_text = '<a href="'+  reverse('idea_detail', args =( idea.id,))
                post_text += '">#' + str(idea.id) + ": "
                post_text += idea.title + "</a>"
                post_text += "<p>" + idea.description + "</p>"
                for image in idea.screenshot_set.all():
                    post_text += '<br /><img src="'+image.image.url+'" height="320" width"240" /><br />'
                post = Post(topic=topic, author=request.user, text=post_text )
                post.save()
                topic.topic_latest_post = post
                topic.posts = 1
                topic.save()
                topic.forum.forum_latest_post = post
                topic.forum.topics += 1
                topic.forum.posts += 1
                topic.forum.save()
                return HttpResponseRedirect(reverse('oi.beyin2.views.main'))
            else:
                return render_response(request, 'beyin2/idea_errorpage.html',{'error':form.errors,})

        else:
            ScreenShotFormSet = ScreenShotSet(prefix = 'imageform')
            return render_response(request, 'beyin2/idea_new.html', {'form':form,'ScreenShotFormSet':ScreenShotFormSet})



@permission_required('beyin2.change_idea')
def edit_idea(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    if idea.status:
        if idea.category:
            form = IdeaForm({'title': idea.title, 'description': idea.description, 'status': idea.status.id, 'category': idea.category.id, 'tags': [tag.id for tag in idea.tags.all()]})
        else:
            form = IdeaForm({'title': idea.title, 'description': idea.description, 'status': idea.status.id, 'tags': [tag.id for tag in idea.tags.all()]})
    else:
        if idea.category:
            form = IdeaForm({'title': idea.title, 'description': idea.description, 'category': idea.category.id, 'tags': [tag.id for tag in idea.tags.all()]})
        else:
            form = IdeaForm({'title': idea.title, 'description': idea.description, 'tags': [tag.id for tag in idea.tags.all()]})
    images = ScreenShot.objects.filter(is_hidden = False, idea = idea )
    if request.POST:
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea.title = form.cleaned_data['title']
            idea.description = form.cleaned_data['description']
            if form.cleaned_data['status']:
                idea.status = form.cleaned_data['status']
            else:
                idea.status = Status()
            if form.cleaned_data['category']:
                idea.category = form.cleaned_data['category']
            else:
                idea.category = Category()
            idea.save()
            idea.topic.title = idea.title
            idea.topic.save()

            idea.tags.clear()
            idea.topic.tags.clear()
            for tag in form.cleaned_data['tags']:
                tag = Tag.objects.get(name=tag)
                idea.tags.add(tag)
                idea.topic.tags.add(tag)

            post_text = '<a href="'+  reverse('idea_detail', args =( idea.id,))
            post_text += '">#' + str(idea.id) + ": "
            post_text += idea.title + "</a>"
            post_text += "<p>" + idea.description + "</p>"
            for image in idea.screenshot_set.all():
                if image.is_hidden == False:
                    post_text += '<br /><img src="'+image.image.url+'" height="320" width"240" /><br />'

            post = idea.topic.post_set.all().order_by('created')[0]

            post.text = post_text
            post.save()

            return HttpResponseRedirect(reverse('oi.beyin2.views.main'))
        else:
            return render_response(request, 'beyin2/idea_errorpage.html')
    else:
        return render_response(request, 'beyin2/idea_edit.html', {'form':form, 'idea':idea,'images':images})

@permission_required('beyin2.change_idea')
def edit_idea_add_image(request,idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    image_form = ScreenShotForm()
    if request.POST:
        image_form_post  = ScreenShotForm(request.POST, request.FILES,)
        if image_form_post.is_valid():
            try:
                image = image_form_post.save(commit = False)
                if image.image:
                    image.idea = idea
                    image.save()
            except:
                return render_response(request, 'beyin2/idea_errorpage.html',{'error': 'image cannot be saved'})
            return HttpResponseRedirect(reverse('oi.beyin2.views.edit_idea', args=(idea.id,)))
        return render_response(request, 'beyin2/idea_errorpage.html',{'error': 'Form is not valid'})
    return render_response(request, 'beyin2/idea_edit_add_image.html', {'image_form':image_form, 'idea':idea})

@permission_required('beyin2.change_idea')
def delete_idea(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    idea.is_hidden = True
    idea.save()

    # and lock the topic from forum
    if idea.topic.locked:
        return render_response(request,'beyin2/idea_errorpage.html',{'error':'Fikir başlığı zaten kilitli?',})
    else:
        idea.topic.locked = 1
        idea.topic.save()

    return HttpResponseRedirect(reverse('oi.beyin2.views.main'))


@permission_required('beyin2.change_idea')
def undelete_idea(request, idea_id):
    idea = Idea.objects.get( pk= idea_id)
    idea.is_hidden = False
    idea.save()

    # unlock the topic
    if not idea.topic.locked:
        return render_response(request,'beyin2/idea_errorpage.html',{'error':'Fikir başlığı kilitli değil?',})
    else:
        idea.topic.locked = 0
        idea.topic.save()

    return HttpResponseRedirect(reverse('oi.beyin2.views.main'))


def mark_duplicate(request, idea_id):
    if request.POST:
        idea = get_object_or_404(Idea, pk = idea_id)
        if request.POST['dupple_number']:
            idea_original = get_object_or_404(Idea, pk= int(request.POST['dupple_number']))
            idea.duplicate = idea_original
        else:
            idea_original = get_object_or_404(Idea, pk = int(request.POST['dupple']))
            idea.duplicate = idea_original
        idea.is_duplicate = True
        idea.save()
        #changes for forum
        #the duplicate
        topic = idea.topic
        post_text = "<h1> Bu fikir başka bir fikrin tekrarı olarak belirlenmiş </h1>"
        post_text += '<a href="'+  reverse('idea_detail', args =( idea_original.id,))
        post_text += '">#' + str(idea_original.id) + ": " + idea_original.title + "</a>"
        post_text += "<p>" + idea_original.description + "</p><br />"
        for image in idea_original.screenshot_set.all():
            if image.is_hidden == False:
                post_text += '<br /><img src="'+image.image.url+'" height="320" width"240" /><br />'
        post_text += "<br /><a href='"+idea_original.topic.get_latest_post_url()+"'>Lütfen buradan devam ediniz...</a>"
        post = Post(topic=topic, author=request.user, text=post_text )
        post.save()
        topic.topic_latest_post = post
        topic.save()
        topic.forum.forum_latest_post = post
        topic.forum.posts += 1
        topic.forum.save()
        #the original idea
        topic = idea_original.topic
        post_text = "<h1> Başka bir fikir bu fikrin tekrarı olarak belirlenmiş </h1>"
        post_text += "<p>#" + str(idea.id) + ": "
        post_text += idea.title + "</p>"
        post_text += "<p>" + idea.description + "</p><br />"
        for image in idea.screenshot_set.all():
            if image.is_hidden == False:
                post_text += '<br /><img src="'+image.image.url+'" height="320" width"240" /><br />'
        post_text += "<br /><a href='"+idea.topic.get_absolute_url()+"'>Daha önce şu başlık altında tartışılmış...</a>"
        post = Post(topic=topic, author=request.user, text=post_text )
        post.save()
        
        post_text = '#' + str(idea.id) + ": " + idea.title
        post_text += "<p>" + idea.description + "</p><br />"
        for image in idea.screenshot_set.all():
            if image.is_hidden == False:
                post_text += '<br /><img src="'+image.image.url+'" height="320" width"240" /><br />'

        post = idea.topic.post_set.all().order_by('created')[0]

        post.text = post_text
        post.save()
        
        topic.topic_latest_post = post
        topic.save()
        topic.forum.forum_latest_post = post
        topic.forum.posts += 1
        topic.forum.save()
        votes_list = Vote.objects.filter( idea = idea)
        for vote in votes_list:
            if vote.vote == "U":
                idea_original.vote_value +=10
            elif vote.vote == "D":
                idea_original.vote_value -=10
            elif vote.vote == "N":
                idea_original.vote_value +=1
            vote.idea = idea_original
            vote.save()

        all_votes = Vote.objects.filter( idea=idea_original ).count()
        all_votes = float(all_votes)
        u_votes = Vote.objects.filter( idea=idea_original, vote="U").count()
        n_votes = Vote.objects.filter( idea=idea_original, vote="N").count()
        d_votes = Vote.objects.filter( idea=idea_original, vote="D").count()
        if all_votes != 0:
            u_percent = int((u_votes/all_votes)*100)
            n_percent = int((n_votes/all_votes)*100)
            d_percent = int((d_votes/all_votes)*100)
        else:
            u_percent = n_percent = d_percent = 0
        percent = (u_percent*1000000)+(n_percent*1000)+d_percent
        idea_original.vote_percent=percent
        idea_original.save()
        return HttpResponseRedirect(reverse('oi.beyin2.views.delete_idea', args=(idea.id,)))
    else:
        idea = get_object_or_404(Idea, pk = idea_id)
        idea_list = Idea.objects.exclude(pk=idea.id).filter(is_hidden=False)
        return render_response(request, 'beyin2/idea_duplicate.html', {'idea': idea,'idea_list': idea_list})

def add_remove_favorite(request,idea_id):
    favorite_user = request.user
    idea = get_object_or_404(Idea, pk = idea_id)
    try:
        favorite = Favorite.objects.filter( user = favorite_user, idea = idea )
        if favorite.count() !=0:
            favorite = favorite[0]
            favorite.delete()
        else:
            favorite = Favorite(user = favorite_user, idea = idea)
            favorite.save()
    except ObjectDoesNotExist:
        favorite = Favorite(user = favorite_user, idea = idea)
        favorite.save()
    return HttpResponse("OK")

def is_favorite(request,idea_id):
    favorite_user = request.user
    idea = get_object_or_404(Idea, pk = idea_id)
    try:
        favorite = Favorite.objects.filter( user = favorite_user, idea = idea )
        if favorite.count() != 0:
            return HttpResponse("YES")
        else:
            return HttpResponse("NO")
    except ObjectDoesNotExist:
        return HttpResponse("NO")

def vote_values_report(request,idea_id):
    idea = get_object_or_404(Idea, pk = idea_id)
    votes_value = idea.vote_value
    vote_percent = idea.vote_percent
    return HttpResponse( "%s_%s" %(idea.vote_value, idea.vote_percent))

def image_remove(request,image_id):
    image = get_object_or_404(ScreenShot, pk = image_id)
    image.is_hidden = True
    image.save()
    return HttpResponse("OK")

