#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import template
from oi.beyin2.models import Vote, Idea

register = template.Library()


@register.inclusion_tag('beyin2/tt_idea_vote.html')
def is_voted(idea,user):
    vote = idea.objects.filter(voter=user)
    return {'vote':vote[0].vote,'idea':idea,'idea':idea}
