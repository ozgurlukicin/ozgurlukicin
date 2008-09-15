#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib import admin
from django.core.exceptions import ValidationError

class CategoryImages(models.Model):
    """ This class has no Meta and Admin class because it's edited inline on related object's page """
    category = models.ForeignKey("Category", blank=True, null=True, related_name="images")
    picture = models.ImageField(verbose_name="Kategori Resmi", upload_to="upload/image/")
    keep = models.BooleanField(default=True, editable=False)
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
    name = models.CharField("İsim", max_length=200)
    slug = models.SlugField("SEF Başlık", help_text="Adres kısmında kullanılan ad, isim kısmından otomatik olarak üretilmektedir")
    # Category can have category inside it, we will get them recursively.
    parent = models.ForeignKey("self", blank=True, null=True, related_name="child")
    description = models.TextField("Kategori açıklaması")

    def get_absolute_url(self):
        return u'/dukkan/kategori/%s/' % self.slug

    def get_active_products(self):
        return self.product_set.filter(active=True)

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
                raise ValidationError("Bir kategoriyi kendisi içerisine yerleştiremezsiniz!")

            for p in self._recurse_for_parents(self):
                if self.id == p.id:
                    raise ValidationError("Bir kategoriyi kendisi içerisine yerleştiremezsiniz!")

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

########################################
#                                      #
# Tax Model that all products can have #
#                                      #
########################################

class Tax(models.Model):
    # FIXME: Maybe inline edited?
    title = models.CharField("Vergi İsmi", max_length=100)
    percentage = models.DecimalField("Vergi Oranı", max_digits=5, decimal_places=2, help_text="3.21 gibi")

    def __unicode__(self):
        return u'%s: %%%s' % (self.title, self.percentage)

    class Meta:
        verbose_name = "Vergi"
        verbose_name_plural = "Vergiler"

######################################################
#                                                    #
# Image class for all Products.                      #
# There is a code repeat but I can't think better :P #
#                                                    #
######################################################

class ProductImages(models.Model):
    """ This class has no Meta and Admin class because it's edited inline on related object's page """
    product = models.ForeignKey("Product", blank=True, null=True, related_name="images")
    picture = models.ImageField(verbose_name="Ürün Resmi", upload_to="upload/image/")
    keep = models.BooleanField(default=True, editable=False)
    # we use remove since we don't have admin interface for editing CategoryImage.
    # It's edited inline on the related model page, when remove is checked, we will just delete the entry.
    remove = models.BooleanField(default=False)

    def __unicode__(self):
        return u'"%s" ürün resmi' % self.product.name

    def save(self):
        # Picture value is always set. When you add new Category without images,
        # it just saves as blank. So prevent adding useless images.

        # new entry.
        if not self.id and not self.picture:
            return
        if self.remove:
            self.delete()
        else:
            super(ProductImages, self).save()

############################################################
#                                                          #
# Main product class, it can have a child product model    #
# It's use-case is T-shirt. A t-shirt can have X/XL/M type #
#                                                          #
############################################################

class Product(models.Model):
    serial = models.CharField("Seri No", help_text="Ürünün seri numarası", max_length=20)
    name = models.CharField("İsim", max_length=200)
    slug = models.SlugField("SEF Başlık", help_text="Adres kısmında kullanılan ad, isim kısmından otomatik olarak üretilmektedir")
    description = models.TextField("Ürün açıklaması")

    stock = models.IntegerField("Ürün Stoğu", default=0)
    price = models.DecimalField("Ürünün fiyatı", default=0, max_digits=5, decimal_places=2, help_text="Ürünün vergisiz fiyatı. Vergi aşağıda seçtiğinize bağlı olarak otomatik bir şekilde bu fiyatın üzerine eklenmektedir. 15.67 gibi YTL cinsinden belirtin.")

    active = models.BooleanField("Aktif", default=False)

    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')
    category = models.ForeignKey('Category', blank=True, null=True)
    tax = models.ForeignKey('Tax', blank=True, null=True)

    def get_absolute_url(self):
        return u'/dukkan/urun/%s/%s/' % (self.category.slug, self.slug)

    def price_with_tax(self):
        return (self.price + (self.price * self.tax.percentage)/100).normalize()

    # used in template's {% if %} statement.
    # it checks whether the product is active and shows if it's active

    def is_active(self):
        return self.active

    def is_in_stock(self):
        return (self.stock > 0)

    # We use them on template
    # If a product have childs (t-shirt, for example), then the page lists these products

    def have_child(self):
        return (self.child.count() > 0)

    def have_parent(self):
        return (self.parent.count() > 0)

    # God damn it, these functions are the same with Category
    # It's a code repeat. Grr..

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

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
