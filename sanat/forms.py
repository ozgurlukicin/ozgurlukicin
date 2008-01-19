#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import zipfile

from django import newforms as forms
import sanat_settings as settings
from oi.sanat.models import  Dosya,SanatScreen,Category,License
import Image
 
vote_choices=(
				(0,u'Berbat'),
				(1,u'Kötü'),
				(2,u'Orta'),
				(3,u'İyi'),
				(4,u'Güzel'),
				(5,u'Süper'),
				)
class VoteForm(forms.Form):
	""" tema vote form validator"""
	vote= forms.ChoiceField(label="Oy",required=True,choices=vote_choices)
    

class ScreenField(forms.Field):
    """ That one will validate the screen upload things"""
    
    def __init__(self,*args,**kwargs):
        """ Calling the upper function"""
        super(ScreenField,self).__init__(*args,**kwargs)
    
    def clean(self,value):
        """ The validator part"""
        #bos musun ?
        super(ScreenField,self).clean(value)
        
        if self.required and not value:
            raise forms.ValidationError(_(u'Bos birakilamaz'))
            
        photo_data=value
        
        
        
        content_type = photo_data.get('content-type')
        
        if content_type:
            
            main,sub=content_type.split('/')
            
            if not (main=='image' and sub in ['jpeg','png','gif']):
                raise forms.ValidationError(_('Sadece JPEG, PNG, GIF'))
                
        size = len (photo_data['content'])
        
        if size > settings.MAX_PHOTO_UPLOAD_SIZE:
            raise forms.ValidationError(_('Resim çok büyük max %s byte'%(settings.MAX_PHOTO_UPLOAD_SIZE)))

        #get the width and height
        #img=Image.open(StringIO.StringIO(photo_data['content']))
        #raise forms.ValidationError(_('Buradayız %s'%(photo_data['dimensions'])))
        width, height = photo_data['dimensions']
        #raise forms.ValidationError(_('Buradayız %s %s'%(width, height)))
        
        if width > settings.MAX_PHOTO_WIDTH:
            raise forms.ValidationError(_('Genişlik çok büyük max %s byte'%(settings.MAX_PHOTO_WIDTH)))
        
        if height > settings.MAX_PHOTO_WIDTH:
            raise forms.ValidationError(_('Yükseklik çok büyük max %s byte'%(settings.MAX_PHOTO_HEIGHT)))
            
        return value

class FileUploadField(forms.Field):
    """ That will validate the files that are uploaded"""
    
    def __init__(self,*args,**kwargs):
        """ Calling the upper function"""
        super(FileUploadField,self).__init__(*args,**kwargs)
    
    
    def clean(self,value):
        """ Tha validator part"""
        super(ScreenField,self).clean(value)
#Burasi file upload kısımları ile alakalı olacak...

class TemaUploadForm(forms.Form):
    """ That form class will handle all the stuff about uploading
    file uploading in 0.96 is not good change it later maybe in 1.0....
    """
    
    parent_category=forms.ChoiceField(label='Kategori', required=True)
    license=forms.ChoiceField(label='Lisans', required=True)
    name=forms.CharField(label="İsim",required=True,max_length=100)
    description=forms.CharField(label="Açıklama",required=True,max_length=100,widget=forms.Textarea())
    
    #file upload kısımları
    screen=ScreenField(widget=forms.FileInput,required=True, label=("Photo"), 
                                    help_text=_("Resim Yükleyiniz (max %s kilobytes) izin verilenler (jpeg,png,gif)"% (settings.MAX_PHOTO_UPLOAD_SIZE)))
                                    
    #file_up=FileUploadField(widget=forms.FileInput(),required=True, label=("Dosya"), 
    #                                help_text=_("Dosya Yükleyiniz (max %s kilobytes) izin verilenler (zip simdlik)"% (settings.MAX_FILE_UPLOAD))) 
    
    
    def __init__(self,*args,**kwargs):
        """ It is for topic tihng they are dinamyc"""
        super(TemaUploadForm, self).__init__(*args, **kwargs)
        
        self.base_fields['parent_category'].choices=[(cat.id, cat.cat_name) for cat in Category.objects.all()]
        self.base_fields['license'].choices=[(l.id, l.name) for l in License.objects.all()]
        
    def save(self):
        """ That part is adding the thning to the system"""
        
        parent_category=self.clean_data['parent_category']
        license=self.clean_data['license']
        name=self.clean_data['name']
        description=self.clean_data['description']
        screen=self.clean_data['screen']
        
        s=SanatScreen(file=screen)
        s.save()
        
        
        d=Dosya(parent_cat=parent_category,licence=licence,user=self.request.user,screens=s,name=name,description=description)
        d.save()
        

