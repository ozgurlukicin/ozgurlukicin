#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User
from oi.st.models import ScreenShot 

# Create your models here.
		
class Category(models.Model):
	""" The categories of thing that are published they maybe 
	neseted in each other a tree hieararchy.."""
	
	#100 is enough for now
	cat_name=models.CharField(max_length=100,verbose_name="Kategori adı",unique=True)
	#if they are nested it is needed
	slug=models.SlugField(verbose_name="SEF Başlık",prepopulate_from=("cat_name",))
	parent_id=models.IntegerField(verbose_name="Ebeveyn Kategori",default=0,choices=self.get_possible_parents())
	update=models.DateField(auto_now=True,verbose_name="Yayın Tarihi")
	
	def __str__(self):
		return self.cat_name
	
	def get_absolute_url(self):
		return "/sanat/kategori/%s/"%(self.slug)
		
	def get_parent_choice(self):
		"""Get the current parent category of the model"""
		return self.parent_id
		
	def get_possible_parents(self):
		""" To have the choices in admin.."""
		temp=[(0,"Kendisi")]
		
		choices=Category.objects.exclude(cat_name=self.cat_name)
		
		if choices:
			for i in choces:
				temp.append((i.id,i.cat_name))
				
		#getting the final value
		return tuple(choices)
				
			
		
	class Admin:
		
		list_display = ('cat_name','parent_id','update')
        	list_filter = ['update']
        	search_fields = ['cat_name']
		ordering=["-id"]
	
	class Meta:
		verbose_name="Kategori"
		verbose_name_plural="Kategoriler"
		
class SanatScreen(ScreenShot):
	"It is modified version because we should change the upload directory ???"
	
	file=models.FileField(upload_to="upload/sanat/images/",default="default.jpg")
	
	class Meta:
		verbose_name="Sanat Görüntü"
		verbose_name_plural="Sanat Görüntü"
		
	class Admin:
		pass

class ArsivDosya(models.Model):
	""" The data file that includes the archives for templates and etc"""
	a_file=models.FileField(upload_to="upload/sanat/dosya/")
	
	class Admin:
		pass
		
	def __str__(self):
		return self.a_file
	
class Dosya(models.Model):
	""" The catual file that will be downloaded and shown"""
	RATE_CHOICES=(
			('0','Yok'),
			('1','Kötü'),
			('2','Orta'),
			('3','İyi'),
			('4','Çok iyi'),
			('5','Süper'),
		)
	
	parent_cat=models.ForeignKey(Category,verbose_name="Kategori")
	licence=models.ForeignKey(Lisans,verbose_name="Lisans")
	user=models.ForeignKey(User,verbose_name="Gönderen")
	
	screens=models.ManyToManyField(SanatScreen,verbose_name="Görüntüler")
	file_data=models.ManyToManyField(ArsivDosya,verbose_name="İçerik Dosyası")
	
	name=models.CharField(max_length=100,unique=True,verbose_name="Dosya ismi")
	description=models.TextField(verbose_name="Açıklama")
	rate=models.CharField(max_length=1,verbose_name="Oy",default="0")
	state=models.BooleanField(verbose_name="Yayınla",default=False)
	counter= models.IntegerField(verbose_name="Sayaç",default=0)
	update=models.DateField(auto_now=True,verbose_name="Yayın Tarihi")
	
	
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return "/sanat/dosya/%s/"%(self.id)
		
	class Admin:
		list_display=('name','rate','state','counter','update','parent_cat')
		search_fields=['name','parent_cat']
		list_filter=['update']
		ordering
		
	
	class Meta:
		ordering=('-update')
		verbose_name="Sanat Dosya"
		verbose_name_plural="Sanat Dosyaları"

