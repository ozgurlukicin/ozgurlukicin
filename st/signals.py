#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 ArtIstanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

def remove_video_thumbnail_on_delete(sender, instance, signal, *args, **kwargs):
    """When video is deleted, remove it's thumbnail too"""
    from oi.settings import MEDIA_ROOT
    from os import remove

    # video filename endswith *.flv and it's thumbnail *.png. so, when we replace *.flv to *.png, we get thumbnail path
    filename = instance.file.replace('.flv', '.png')
    remove(MEDIA_ROOT + filename)

def open_forum_topic(sender, instance, signal, *args, **kwargs):
    """When we add a news we should open a new topic in forum with the same text"""
    from django.contrib.auth.models import User
    from oi.forum.models import Forum,Topic,Post
    from oi.middleware import threadlocals

    user=User.objects.filter(username=threadlocals.get_current_user())

    #gerekenler :howto,game,package,news ??? _meta.module_name

    #lets make it more flexible:
    if instance._meta.module_name=="howto":
        name="Nasıl"
    elif instance._meta.module_name=="game":
        name="Oyunlar"

    elif instance._meta.module_name=="package":
        name="Paketler"

    elif instance._meta.module_name=="news":
        name="Haberler"

    forum=Forum.objects.filter(name=name)

    ch=sender.objects.filter(id=instance.id)
    #if it is a new newss
    if not ch:
        if instance.status and forum and user:

            topic = Topic(forum=forum[0],
                                  title=instance.title #or any
                                 )
            topic.save()

            post = Post(topic=topic,
                                author=user[0],
                                text=instance.text
                               )
            post.save()
            topic.topic_latest_post = post
            topic.save()

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
                    for tag in instance.tags.all():
                        topic.tags.add(tag)

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
