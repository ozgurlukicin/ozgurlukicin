#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.shop.product.models import CategoryImages, Category, Tax, ProductImages, Product

class CategoryImagesInline(admin.TabularInline):
    model = CategoryImages
    max_num = 2

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name", "slug"]
    list_display = ("name", "_parents_repr",)
    prepopulate_fields = {"slug":("name",)}
    inlines = [CategoryImagesInline]

class TaxAdmin(admin.ModelAdmin):
    list_display = ("title", "percentage",)
    search_fields = ['title']
    ordering = ['title']

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    max_num = 3

class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Ürün Bilgileri", {"fields": ("serial", "name", "slug", "description", "stock", "price")}),
        ("Kategori/Resim/Vergi", {"fields": ("parent", "category", "tax")}),
        (None, {"fields": ("active",)})
        )
    search_fields = ["serial", "name"]
    list_filter = ["active"]
    list_display = ("name", "stock", "_parents_repr", "category", "active")
    prepopulate_fields = {"slug":("name",)}
    inlines = [ProductImagesInline]
    ordering = ["name", "price"]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Product, ProductAdmin)
