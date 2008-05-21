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
import settings
from oi.tema.models import  File,Thumbnail,Category,License,ArchiveFile
import Image
from django.shortcuts import get_object_or_404

vote_choices=(
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        )

class VoteForm(forms.Form):
    """tema vote form validator"""
    vote= forms.ChoiceField(label="Oy", required=True, choices=vote_choices)

class ScreenField(forms.Field):
    """That one will validate the screen upload things"""

    def clean(self,value):
        """The validator part"""
        #bos musun ?
        super(ScreenField,self).clean(value)

        if self.required and not value:
            raise forms.ValidationError(u'Boş bırakılamaz')

        photo_data=value

        content_type = photo_data.get('content-type')

        if content_type:

            main,sub=content_type.split('/')

            if not (main=='image' and sub in ['jpeg','png','gif']):
                raise forms.ValidationError('Sadece JPEG, PNG, GIF türleri kabul ediliyor')

        size = len (photo_data['content'])

        if size > settings.MAX_PHOTO_UPLOAD_SIZE:
            raise forms.ValidationError('Resim boyutu çok büyük, en fazla %s bayt olabilir'%(settings.MAX_PHOTO_UPLOAD_SIZE))

        #get the width and height

        width, height = photo_data['dimensions']
        #raise forms.ValidationError(_('Buradayız %s %s'%(width, height)))

        if width > settings.MAX_PHOTO_WIDTH:
            raise forms.ValidationError('Genişlik çok büyük, en fazla %s piksel olabilir'%(settings.MAX_PHOTO_WIDTH))

        if height > settings.MAX_PHOTO_WIDTH:
            raise forms.ValidationError('Yükseklik çok büyük, en fazla %s piksel olabilir'%(settings.MAX_PHOTO_HEIGHT))

        return value

class FileUploadField(forms.Field):
    """ That will validate the files that are uploaded"""

    def __init__(self,*args,**kwargs):
        """ Calling the upper function"""
        super(FileUploadField,self).__init__(*args,**kwargs)


    def clean(self,value):
        """ Tha validator part"""
        super(FileUploadField,self).clean(value)

        if self.required and not value:
            raise forms.ValidationError(u'Boş bırakılamaz')

        file_data=value

        content_type = file_data.get('content-type')

        if content_type:
            if content_type!='application/zip':
                msg = 'Şimdilik sadece zip türündeki dosyalara izin veriyoruz!'
                raise forms.ValidationError(msg)

            zip = zipfile.ZipFile(StringIO.StringIO(file_data['content']))
            bad_file = zip.testzip()
            zip.close()
            del zip
            if bad_file:
                msg = '"%s" sıkıştırılmış dosya bozuk' % (bad_file,)
                raise forms.ValidationError(msg)

            return file_data

        else:
            raise forms.ValidationError("Gönderdiğiniz dosya bozuk olabilir")

#The file upload thing

class TemaUploadForm(forms.Form):
    """
    That form class will handle all the stuff about uploading
    file uploading in 0.96 is not good change it later maybe in 1.0....
    """

    parent_category=forms.ChoiceField(label='Kategori', required=True)
    license=forms.ChoiceField(label='Lisans', required=True)
    name=forms.CharField(label="İsim",required=True,max_length=100)
    description=forms.CharField(label="Açıklama",required=True,max_length=100,widget=forms.Textarea())

    #file upload kısımları
    screen=ScreenField(widget=forms.FileInput(),required=True, label="Ekran Görüntüsü",
            help_text="En fazla %sKB boyutunda bir jpeg, png veya gif resmi olabilir"% (settings.MAX_PHOTO_UPLOAD_SIZE))
    file_up=FileUploadField(widget=forms.FileInput(),required=True, label="Dosya",
            help_text="En fazla %sKB, olabilir zip biçiminde"% (settings.MAX_FILE_UPLOAD))

    def __init__(self,*args,**kwargs):
        """ Collect licenses and categories"""
        super(TemaUploadForm, self).__init__(*args, **kwargs)
        self.fields['license'].choices=[(int(l.id), l.name) for l in License.objects.all()]
        self.fields['parent_category'].choices=[(int(cat.id), cat.cat_name) for cat in Category.objects.all()]

    def save(self):
        """ That part is adding the thning to the system"""

        parent_category=self.cleaned_data['parent_category']
        license=self.cleaned_data['license']
        name=self.cleaned_data['name']
        description=self.cleaned_data['description']
        screen=self.cleaned_data['screen']
        user=screen['user']
        file=self.cleaned_data['file_up']

        s=Thumbnail()
        s.save_file_file(screen['filename'],screen['content'])

        #buraya arsiv dosyası işlemi gelecek
        a=ArchiveFile()
        a.save_a_file_file(file['filename'],file['content'])

        cat=get_object_or_404(Category, pk=parent_category)
        li=get_object_or_404(License, pk= license)

        d=File(parent_cat=cat,licence=li,user=user,name=name,description=description,enable_comments=True)
        d.save()
        d.screens.add(s)
        d.file_data.add(a)
