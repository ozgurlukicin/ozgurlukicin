#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.core import validators

class CategoryImages(models.Model):
    """ This class has no Meta and Admin class because it's edited inline on related object's page """
    category = models.ForeignKey("Category", blank=True, null=True, edit_inline=models.TABULAR, num_in_admin=2, max_num_in_admin=2, related_name="images")
    picture = models.ImageField(verbose_name="Kategori Resmi", upload_to="upload/image/")
    keep = models.BooleanField(default=True, editable=False, core=True)
    # we use remove since we don't have admin interface for editing CategoryImage.
    # It's edited inline on the related model page, when remove is checked, we will just delete the entry.
    remove = models.BooleanField(default=False)

    def __unicode__(self):
        return u'"%s" kategori resmi' % self.category.name

    def save(self):
        # Picture value is always set. When you add new Category without images,
        # it just saves as blank. So prevent adding useless images.

        # new entry.
        if not self.id and not self.picture:
            return
        if self.remove:
            self.delete()
        else:
            super(CategoryImages, self).save()

class Category(models.Model):
    """ Base category model for all products """
    name = models.CharField("İsim", max_length=200, core=True)
    slug = models.SlugField("SEF Başlık", help_text="Adres kısmında kullanılan ad, isim kısmından otomatik olarak üretilmektedir", prepopulate_from=("name",))
    # Category can have category inside it, we will get them recursively.
    parent = models.ForeignKey("self", blank=True, null=True, related_name="child")
    description = models.TextField("Kategori açıklaması")

    def get_absolute_url(self):
        return u'/dukkan/kategori/%s/' % self.slug

    def have_child(self):
        if self.child.count() > 0:
            return True
        else:
            return False

    def have_parent(self):
        if not self.parent_id:
            return False
        else:
            return True

    def get_separator(self):
        return ' :: '

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

    def _flatten(self, L):
        """
        Taken from a python newsgroup post
        """
        if type(L) != type([]): return [L]
        if L == []: return L
        return self._flatten(L[0]) + self._flatten(L[1:])

    def _recurse_for_children(self, node):
        children = []
        children.append(node)
        for child in node.child.all():
            if child != self:
                children_list = self._recurse_for_children(child)
                children.append(children_list)
        return children

    def get_all_children(self):
        """
        Gets a list of all of the children categories.
        """
        children_list = self._recurse_for_children(self)
        flat_list = self._flatten(children_list[1:])
        return flat_list

    class Meta:
        ordering = ["name"]
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    class Admin:
        search_fields = ["name", "slug"]
        list_display = ("name", "_parents_repr",)
