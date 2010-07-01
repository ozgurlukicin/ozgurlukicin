#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.http import HttpResponse, HttpResponseRedirect
from oi.beyin2.models import Idea, Status, Category
from oi.beyin2.forms import IdeaForm
from oi.st.wrappers import render_response
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from oi.forum.models import Topic, Forum, Post

DefaultCategory = 4
DefaultStatus = 3
ForumCategory = "Yeni Fikirler"

def main(request):
    idea_list = Idea.objects.filter(is_hidden=False).order_by('-dateSubmitted')[:10]
    return render_response(request,'beyin2/idea_list.html',{'idea_list': idea_list})

@login_required
def add_new(request):
    try:
        form = IdeaForm({'title': '', 'description': '', 'status': DefaultStatus, 'category': DefaultCategory})
        if request.POST:
            form = IdeaForm(request.POST)
            if form.is_valid():
                forum = Forum.objects.get(name = ForumCategory)
                topic = Topic(forum = forum,title = form.cleaned_data['title'])
                topic.save()

                idea = form.save(commit = False)
                idea.submitter = request.user
                idea.topic = topic
                idea.save()

                post_text = "<p>#" + str(idea.id) + " "
                post_text += idea.title + "</p>"
                post_text += "<p>" + idea.description + "</p>"
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
                return render_response(request, 'beyin2/idea_errorpage.html')
        else:
            return render_response(request, 'beyin2/idea_new.html', {'form':form,})
    except:
        return render_response(request, 'beyin2/idea_errorpage.html')

@permission_required('beyin2.change_idea')
def edit_idea(request, idea_id):
    try:
        idea = get_object_or_404(Idea, pk=idea_id)
        form = IdeaForm({'title': idea.title, 'description': idea.description, 'status': idea.status.id, 'category': idea.category.id})
        if request.POST:
            form = IdeaForm(request.POST)
            if form.is_valid():
                """
                i = form.save(commit = False, instance=idea)
                i.submitter = request.user
                
                i.save()
                """
                i = IdeaForm(request.POST, instance = idea)
                i.save()
                return HttpResponseRedirect(reverse('oi.beyin2.views.main'))
            else:
                return render_response(request, 'beyin2/idea_errorpage.html')
        else:

            return render_response(request, 'beyin2/idea_edit.html', {'form':form, 'idea':idea})
    except:
        return render_response(request, 'beyin2/idea_errorpage.html')


def delete_idea(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    idea.is_hidden = True
    idea.save()
    return HttpResponseRedirect(reverse('oi.beyin2.views.main'))


