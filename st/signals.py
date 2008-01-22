#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 ArtIstanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

def open_forum_topic(sender, instance, signal, *args,**kwargs):
    """When we add a news we should open a new topic in forum with the same text"""
    from django.contrib.auth.models import User
    from oi.forum.models import Forum,Topic,Post
    
    user=User.objects.filter(username="admin")
    forum=Forum.objects.filter(name="Haberler")
    
    ch=sender.objects.filter(id=instance.id)
    #if it is a new newss
    if not ch:
        if instance.status and forum and user:
            
            topic = Topic(forum=forum[0],
                                  title=instance.title #news title
                                 )
            topic.save()

            post = Post(topic=topic,
                                author=user[0],
                                text=instance.text
                               )
            post.save()
            
        else:
            return
    
    else: # eger orada varsa ve bu bir edit ise yani sonradan aktif yapıldıysa ...
        if ch[0].status==False and instance.status==True:
            t=Topic.objects.filter(title=ch[0].title) #önceden varsa elleme
            if not t:
                if forum and user:
                    topic = Topic(forum=forum[0],
                                  title=instance.title #news title
                                 )
                    topic.save()

                    post = Post(topic=topic,
                                author=user[0],
                                text=instance.text
                               )
                    post.save()
                else:    
                    return
            else:
                return
        else:
            return
                
            
            
