#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.core import validators

class Category(models.Model):
    """ Base category model for all products """
    name = models.CharField("İsim", max_length=200, core=True)
    slug = models.SlugField("SEF Başlık", help_text="Adres kısmında kullanılan ad, isim kısmından otomatik olarak üretilmektedir", prepopulate_from=("name",))
    # Category can have category inside it, we will get them recursively.
    parent = models.ForeignKey("self", blank=True, null=True, related_name="child")
    description = models.TextField("Kategori açıklaması")

    def _recurse_for_parents(self, cat_obj):
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(p)
            if p != self:
                more = self._recurse_for_parents(p)
                p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def get_separator(self):
        return ' :: '

    # For displaying object's parents on admin page correctly
    def _parents_repr(self):
        name_list = [cat.name for cat in self._recurse_for_parents(self)]
        return self.get_separator().join(name_list)
    _parents_repr.short_description = "Category parents"

    def __unicode__(self):
        name_list = [cat.name for cat in self._recurse_for_parents(self)]
        name_list.append(self.name)
        return self.get_separator().join(name_list)

    # override save() method to check whether the same object is selected for an object's parent
    def save(self):
        if self.id:
            if self.parent and self.parent_id == self.id:
                raise validators.ValidationError("Bir kategoriyi kendisi içerisine yerleştiremezsiniz!")

            for p in self._recurse_for_parents(self):
                if self.id == p.id:
                    raise validators.ValidationError("Bir kategoriyi kendisi içerisine yerleştiremezsiniz!")

        super(Category, self).save()

    class Meta:
        ordering = ["name"]
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    class Admin:
        search_fields = ["name", "slug"]
        list_display = ("name", "_parents_repr",)
