#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Uğur Çetin
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.


from django import template
from oi.petition.models import Petitioner

register = template.Library()

class PetitionBox(template.Node):
    def __init__(self, petitionpercent, numberofpetitioners):
        self.formatdict = {
                "petitionpercent": petitionpercent,
                "numberofpetitioners": numberofpetitioners,
                }
    def render(self, content):
        return """
        <div class="sidebar_bottom_content">
            <a href="/ooxml/"><img src="/media/ooxml/ooxmlekarsi.png" alt="Özgürlükİçin OOXML'e karşı" /></a>
            <p><a href="/ooxml/">"Özgürlükİçin OOXML'e Hayır!"</a> diyoruz. <a href="/ooxml_banner/">Banner ve düğmelerimizi</a> kullanarak kampanyamıza katkıda bulunabilir ve manifestomuzu destekleyerek siz de OOXML'e hayır diyebilirsiniz.</p>
            <div id="ooxmlbar"><div id="ooxmlbar_completed" style="width:%(petitionpercent)s%%;">&nbsp;</div></div>
            <p>Destekleyenler: %(numberofpetitioners)s / 3000</p>
        </div>
""" % self.formatdict

@register.tag
def petition_box(parser, token):
    """ returns a petition box for oi sidebar """
    numberofpetitioners = Petitioner.objects.filter(is_active=True).count()
    petitionpercent = numberofpetitioners / 30
    if petitionpercent > 100:
        petitionpercent = 100
    return PetitionBox(petitionpercent, numberofpetitioners)
