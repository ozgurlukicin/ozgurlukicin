from django import template
from django.core.urlresolvers import reverse



register = template.Library()
@register.inclusion_tag('beyin2/tt_idea_vote.html')
def is_voted(idea, user, come_from):
    vote = idea.vote_set.filter( voter=user )
    if vote:
        return {'idea':idea,'vote':vote[0].vote, 'come_from':come_from}
        #if not exist send Y
    else:
        return {'idea':idea,'vote': "Y", 'come_from': come_from}


@register.inclusion_tag('beyin2/tt_idea_vote_return.html')
def vote_value_calc(idea_to_calc):
    vote_value = idea_to_calc.vote_value//10
    yes_percent = int(round(idea_to_calc.vote_percent/1000000))
    notr_percent = int(round((idea_to_calc.vote_percent-yes_percent*1000000)/1000))
    no_percent = int(round((idea_to_calc.vote_percent-yes_percent*1000000-notr_percent*1000)))
    yes_width = yes_percent*60/100
    notr_width = notr_percent*60/100
    no_width = no_percent*60/100
    return {'vote_value':vote_value, 'yes_percent':yes_percent, 'notr_percent':notr_percent, 'no_percent':no_percent}
