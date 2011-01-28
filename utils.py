#!/usr/bin/python
# -*- coding: utf-8 -*-

TURKISH_CHARS = (
    (u"ç", "c"),
    (u"ğ", "g"),
    (u"ı", "i"),
    (u"ö", "o"),
    (u"ş", "s"),
    (u"ü", "u"),
    (u"Ç", "c"),
    (u"Ğ", "g"),
    (u"İ", "i"),
    (u"Ö", "o"),
    (u"Ş", "s"),
    (u"Ü", "u"),
    (u" ", "_"),
    )

def replace_turkish(text):
    for i in TURKISH_CHARS:
        text = text.replace(i[0], i[1])
    return text
