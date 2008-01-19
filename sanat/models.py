#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

#Requires..
from django.db import models
from django.contrib.auth.models import User
from oi.st.models import License
from django.db.models import signals
from django.dispatch import dispatcher
from oi.sanat.signals import rm_thumb,crt_thumb,rmv_files

from oi.comments.moderation import CommentModerator, moderator


class Category(models.Model):
	""" The categories of thing that are published they maybe 
	neseted in each other a tree hieararchy.."""
	
	#100 is enough for now
	cat_name=models.CharField(maxlength=100,verbose_name="Kategori adı",unique=True)
	#if they are nested it is needed
	slug=models.SlugField(verbose_name="SEF Başlık",prepopulate_from=("cat_name",))
	parent_id=models.IntegerField(verbose_name="Ebeveyn Kategori",default=0)
	update=models.DateField(auto_now=True,verbose_name="Yayın Tarihi")
	
	def __str__(self):
		return self.cat_name
	
	def get_absolute_url(self):
		return "/tema/kategori/%s/"%(self.slug)
		
	def get_parent_choice(self):
		"""Get the current parent category of the model"""
		return self.parent_id

	def get_possible_parents(self,cls):
		""" To have the choices in admin.."""
		temp=[(0,"Kendisi")]
		
		choices=cls.objects.all()
		
		if choices:
			for i in choices:
				temp.append((i.id,i.cat_name))
				
		#getting the final value
		return tuple(choices)
		
	#get_possible_parents=staticmethod(get_possible_parents)
				
	class Admin:
		
		list_display = ('cat_name','parent_id','update')
        list_filter = ['update']
        search_fields = ['cat_name']
        ordering=["-id"]
	
	class Meta:
		verbose_name="Kategori"
		verbose_name_plural="Kategoriler"
		

		
	
		
class SanatScreen(models.Model):
	"It is modified version because we should change the upload directory ???"
	
	file=models.FileField(upload_to="upload/sanat/images/",blank=True)
	
	class Meta:
		verbose_name="Sanat Görüntü"
		verbose_name_plural="Sanat Görüntü"
		
	def __str__(self):
		return self.file 
	
	class Admin:
		
		pass
	
# when we add or delete a thumb it is needed
dispatcher.connect(crt_thumb,signal=signals.post_save, sender=SanatScreen)
dispatcher.connect(rm_thumb,signal=signals.post_delete, sender=SanatScreen)


class ArsivDosya(models.Model):
    """ The data file that includes the archives for templates and etc"""
    a_file=models.FileField(upload_to="upload/sanat/dosya/")
    #download=models.IntegerField(verbose_name="İndirilme",default=0)
    
    class Admin:
		pass
    
    def __str__(self):
		return self.a_file
	
class Dosya(models.Model):
	""" The catual file that will be downloaded and shown"""
	
	parent_cat=models.ForeignKey(Category,verbose_name="Kategori")
	licence=models.ForeignKey(License,verbose_name="Lisans")
	user=models.ForeignKey(User,verbose_name="Gönderen")
	
	screens=models.ManyToManyField(SanatScreen,verbose_name="Görüntüler",blank=True)
	file_data=models.ManyToManyField(ArsivDosya,verbose_name="İçerik Dosyası",blank=True)
	
	name=models.CharField(maxlength=100,unique=True,verbose_name="Dosya ismi")
	description=models.TextField(verbose_name="Açıklama")
	rate=models.FloatField(verbose_name="Puan",default=0,max_digits=2, decimal_places=1)
	state=models.BooleanField(verbose_name="Yayınla",default=False)
	counter= models.IntegerField(verbose_name="Sayaç",default=0)
	update=models.DateField(auto_now=True,verbose_name="Yayın Tarihi")
	
	#added later ...
	enable_comments = models.BooleanField()
	
	
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return "/tema/dosya/%s/"%(self.id)
	
	class Admin:
		list_display=('name','rate','state','counter','update','parent_cat')
		search_fields=['name','parent_cat']
		list_filter=['update']
		ordering=['-update']
		
	
	class Meta:
		
		verbose_name="Sanat Dosya"
		verbose_name_plural="Sanat Dosyaları"

dispatcher.connect(rmv_files,signal=signals.pre_delete, sender=Dosya)

#dont forget to disable it before uploading pff
class DosyaCommentModerator(CommentModerator):
	""" Dosya models class Comment moderation""",
	akismet = False
	email_notification = False
	enable_field = 'enable_comments'
	
#register it 
moderator.register(Dosya, DosyaCommentModerator)
