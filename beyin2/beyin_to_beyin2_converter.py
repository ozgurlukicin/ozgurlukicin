#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import oi.ideas.models
import oi.beyin2.models
from oi.st.models import Tag
from django.core.urlresolvers import reverse

def convert():
    ideas_idea_list = oi.ideas.models.Idea.objects.all()
    
    prefered_status = [4, 5, 6, 7]
    
    for ideas_idea in ideas_idea_list:
        if ideas_idea.status.id in prefered_status:
            if ideas_idea.is_duplicate == True:
                ideas_idea.is_hidden = True
            beyin2_idea = oi.beyin2.models.Idea(
                                                title = ideas_idea.title, 
                                                dateSubmitted = ideas_idea.submitted_date, 
                                                submitter = ideas_idea.submitter, 
                                                description = ideas_idea.description, 
                                                is_hidden = ideas_idea.is_hidden, 
                                                is_duplicate = ideas_idea.is_duplicate,
                                                topic = ideas_idea.topic,
                                               )
            beyin2_idea.save()
            beyin2_idea.topic.title = beyin2_idea.title
            beyin2_idea.topic.save()
            
            for tag in ideas_idea.tags.all():
                    tags = Tag.objects.filter(name=tag)
                    for tag in tags:
                        beyin2_idea.tags.add(tag)
                        beyin2_idea.topic.tags.add(tag)
            
            post_text = '<a href="'+  reverse('idea_detail', args =( beyin2_idea.id,))
            post_text += '">#' + str(beyin2_idea.id) + " "
            post_text += beyin2_idea.title + "</a>"
            post_text += "<p>" + beyin2_idea.description + "</p>"
            
            post = beyin2_idea.topic.post_set.all().order_by('created')[0]
            
            post.text = post_text
            post.save()

def del_old():
    oi.beyin2.models.Idea.objects.all().delete()
    oi.beyin2.models.ScreenShot.objects.all().delete()

