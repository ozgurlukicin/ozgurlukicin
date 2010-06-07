#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

from oi.shop.product.models import Product

class CartItem(models.Model):
    quantity = models.PositiveIntegerField("Adet")
    product = models.ForeignKey(Product, verbose_name="Ürün")

class Cart(models.Model):
    """ A Cart contains items that user is going buy """
    user = models.ForeignKey(User, unique=True)
    items = models.ManyToManyField(CartItem, verbose_name="Satın Alınanlar")
