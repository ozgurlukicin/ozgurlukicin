#!/usr/bin/python
# -*- coding: utf-8 -*-

import locale

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from django.template import Context, loader

from oi.shipit.models import CdClient

locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")

clients = CdClient.objects.filter(confirmed=True, sent=False)[:16]

c = canvas.Canvas("cdclients.pdf", A4)
pdfmetrics.registerFont(TTFont("DejaVu Sans Condensed", "/usr/share/fonts/dejavu/DejaVuSansCondensed.ttf"))
c.setFont("DejaVu Sans Condensed", 10)

paragraphStyle = ParagraphStyle({})
paragraphStyle.fontName = "DejaVu Sans Condensed"
paragraphStyle.fontSize = 9

counter = 0
for client in clients[:16]:
    if counter%2:
        start = (350, 45+97*(counter/2))
    else:
        start = (50, 45+97*(counter/2))
    c.drawString(start[0], start[1], "TEL: %s" % client.get_full_phone())
    c.drawString(start[0], start[1]+12, "%s %s/%s" % (client.postcode, client.town.title(), client.get_city_display()))
    paragraph = Paragraph(client.address, paragraphStyle)
    paragraph.split(190, 40)
    paragraph.drawOn(c, start[0], start[1]+24)
    c.drawString(start[0], start[1]+60, client.get_full_name())
    c.drawString(start[0]+150, start[1]+60, "#%s" % client.get_id())
    counter += 1

c.showPage()
c.save()
