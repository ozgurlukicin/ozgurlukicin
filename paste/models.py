#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound
from django.utils.translation import ugettext as _

LANGUAGES = (
    ('bash', 'Bash'),
    ('c', 'C'),
    ('css', 'CSS'),
    ('html', 'HTML'),
    ('ini', 'INI'),
    ('java', 'Java'),
    ('js', 'JavaScript'),
    ('perl', 'Perl'),
    ('php', 'PHP'),
    ('python', 'Python'),
    ('rb', 'Ruby'),
    ('sql', 'SQL'),
    ('text', _('Plain text')),
    ('xml', 'XML'),
)

class PastedText(models.Model):
    text = models.TextField("Yazı", max_length=250000, help_text=_("250000 characters at most"))
    author = models.ForeignKey(User, verbose_name=_("Author"))
    ip = models.IPAddressField(_("IP Address"), blank=True)
    date = models.DateTimeField(_("Date"), auto_now_add=True)
    is_hidden = models.BooleanField(_("Hidden"), default=False)
    syntax = models.CharField(_("Syntax"), max_length=10, choices=LANGUAGES, default="text")
    highlighted_text = models.TextField(_("Colorified Text"), blank=True, editable=False)

    def __unicode__(self):
        return text[:20]

    class Meta:
        permissions = (
            ("hide_pastedtext", _("Can hide pasted text")),
        )

    def highlight(self):
        formatter = HtmlFormatter(linenos = 'table', lineanchors = 'line', linenospecial = 5)
        highlighted = ""
        if self.syntax == "text":
            try:
                highlighted = highlight(self.text, guess_lexer(self.text), formatter)
            except ClassNotFound:
                highlighted = highlight(self.text, get_lexer_by_name("text"), formatter)
        else:
            highlighted = highlight(self.text, get_lexer_by_name(self.syntax), formatter)
        return highlighted

    def save(self):
        self.highlighted_text = self.highlight()
        super(PastedText, self).save()

    def get_absolute_url(self):
        return "/yapistir/%d/" % self.id

    def get_hide_url(self):
        return "/yapistir/%d/hide/" % self.id

    def get_toggle_url(self):
        return "/yapistir/%d/toggle/" % self.id
