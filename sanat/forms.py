#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import newforms as forms
import sanat_settings as settings
 
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
    

#Burasi file upload kısımları ile alakalı olacak...

class TemaUploadForm(forms.Form):
    """ That form class will handle all the stuff about uploading
    file uploading in 0.96 is not good change it later ....
    """
    
    parent_category=forms.ChoiceField(label='Kategori', required=True)
    licence=forms.MultipleChoiceField(label='Lisans', required=True)
    name=forms.CharField(label="İsim",required=True,max_length=100)
    description=forms.CharField(label="Açıklama",required=True,max_length=100,widget=forms.Textarea())
    
    #file upload kısımları
    screen=forms.Field(widget=forms.FileInput,required=True, label=("Photo"), 
                                    help_text=_("‘Upload an image (max %s kilobytes)"% settings.MAX_PHOTO_UPLOAD_SIZE))
                                    
    file_up=forms.Field(widget=forms.FileInput()) #yeterrrr
    
    def __init__(self,*args,**kwargs):
        """ It is for topic tihng they are dinamyc"""
        super(TemaUploadForm, self).__init__(*args, **kwargs)
        self.base_fields['parent_category'].choices=[(cat.id, cat.cat_name) for cat in Category.objects.all()]
        self.base_fields['license'].choices=[(l.id, l.name) for l in License.objects.all()]

