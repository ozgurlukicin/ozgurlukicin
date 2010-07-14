#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import oi.ideas.models
import oi.beyin2.models
from django.core.urlresolvers import reverse

def convert():
    ideas_idea_list = oi.ideas.models.Idea.objects.all()
    i = 0
    for ideas_idea in ideas_idea_list:
        i += 1
        beyin2_idea = oi.beyin2.models.Idea(title = ideas_idea.title, 
                                            dateSubmitted = ideas_idea.submitted_date, 
                                            submitter = ideas_idea.submitter, 
                                            description = ideas_idea.description, 
                                            is_hidden = ideas_idea.is_hidden, 
                                            topic = ideas_idea.topic)
        beyin2_idea.save()
        beyin2_idea.topic.title = beyin2_idea.title
        beyin2_idea.topic.save()
        
        post_text = '<a href="'+  reverse('idea_detail', args =( beyin2_idea.id,))
        post_text += '">#' + str(beyin2_idea.id) + " "
        post_text += beyin2_idea.title + "</a>"
        post_text += "<p>" + beyin2_idea.description + "</p>"
        
        post = beyin2_idea.topic.post_set.all().order_by('created')[0]
        
        post.text = post_text
        post.save()
        if i == 100:
            break