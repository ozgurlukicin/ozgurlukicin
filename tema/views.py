#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 ArtIstanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

# Create your views here.
from django.views.generic.list_detail import object_list
from settings import HOME_ITEMS
from oi.tema.models import Dosya,Category
from django.shortcuts import render_to_response,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from oi.tema.forms import VoteForm,TemaUploadForm
from django.core.urlresolvers import reverse

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import Image

def list_material(request,sort_by="son"):
    """ That view vill show the ones that are submitted and approved by admin
    sort_by parameter is the part that tells which one will be shown..."""

    valid_sorts=["son","begenilen","indirilen"]

    if request.method == 'GET':
        if sort_by in valid_sorts:

            if sort_by == "son":
                sorgu=Dosya.objects.filter(state=True).order_by("update")

            elif sort_by == "begenilen":
                sorgu=Dosya.objects.filter(state=True).order_by("-rate")

            elif sort_by == "indirilen":
                sorgu=Dosya.objects.filter(state=True).order_by("-counter")

            params={

                'queryset':sorgu,
                'paginate_by':HOME_ITEMS,
                'template_name':'tema/main.html',

                    }


            #en son burasi
            return object_list(request,**params)


        else:
            #not valid option
            return render_to_response('404.html')

    else :
        # no way
        return render_to_response('404.html')


def list_category(request,cat_name):
    """ List the files according to their parent category"""
    import re

    #hav to thing a little bit about sec
    x=re.compile(r"([a-z])[a-z\-\_]*([a-z])")
    res=re.match(x,cat_name.strip())

    #if doesnt pass the test ...
    if not res:
        return render_to_response('404.html')


    res=Category.objects.filter(slug=cat_name)

    if not res:
        return render_to_response('404.html')

    sorgu=res[0].dosya_set.filter(state=True)

    params={

                'queryset':sorgu,
                'paginate_by':HOME_ITEMS,
                'template_name':'tema/main.html',

                    }

    return object_list(request,**params)


def file_detail(request,file_id):
    """" Shows the details of the file"""

    #we know it is a int
    dosya = get_object_or_404(Dosya, pk=file_id)

    dosya.counter +=1
    dosya.save()

    auth=False

    if request.user.is_authenticated():
        auth=request.user.username

    return render_to_response('tema/detail.html', {'dosya':dosya,'auth':auth,'form':VoteForm()})


def list_user(request,username):
    """ Lists a users things that he/she uploaded to site"""

    u=User.objects.filter(username=username)

    if not u:
        return render_to_response('404.html')

    sorgu=u[0].dosya_set.filter(state=True)

    #sorgu=Dosya.objects.filter(user=username,state=True)

    params={

                'queryset':sorgu,
                'paginate_by':HOME_ITEMS,
                'template_name':'tema/main.html',

                    }

    return object_list(request,**params)


@login_required
def add_file(request):
    """ That one will add a file to the system the hardest one !buraya ayrica permssion da eklenecek."""

    if request.method== 'POST' and request.user.has_perm('dosya.can_upload_tema'): # bu kısmı başka yere yönlendirr

        if "screen" in request.FILES:

            try :
                img= Image.open(StringIO.StringIO(request.FILES['screen']['content']))
                request.FILES['screen']['dimensions'] = img.size
                request.FILES['screen']['user']=request.user
            except :
                request.FILES['screen']['error'] = True

            new_data = request.POST.copy()

            new_data.update(request.FILES)
            #new_data.setlist('parent_category',[int(request.POST['parent_category'].strip())])

            form=TemaUploadForm(new_data)
            #return render_to_response('tema/upload.html',{'form':form,'extralar':new_data['parent_category'],'secenek':form.base_fields['parent_category'].choices})
            if form.is_valid():

                #save all the things
                form.save()

                sort_by="son"
                #return render_to_response('tema/upload.html',{'form':form})
                #return HttpResponseRedirect(reverse(viewname="oi.tema.views.list_category",args=[sort_by]))
                return HttpResponseRedirect("/tema/goster/begenilen/")
        else:
            form=TemaUploadForm()

    else:
        form=TemaUploadForm()
    return render_to_response('tema/upload.html',{'form':form})







@login_required
def vote_it(request):
    """ That one is for voting thing for uploaded files
    Also pass the id of detail you are looking at to pass it to previous page!"""

    #<input type="hidden" name="dosya_id" value="{{ dosya.id }}"



    if request.method== 'POST':

        #we dont want nasty users :)
        if not request.POST.has_key('dosya_id'):
            return render_to_response('404.html')

        try:
            d_id=int(request.POST['dosya_id'])
        except Exception:
            render_to_response('404.html')


        dosya = get_object_or_404(Dosya, pk=d_id)
        auth=dosya.user.username



        if request.session.get(d_id):
            #it was voted before #should add a new error arg
            return render_to_response('tema/detail.html',{'dosya':dosya,'auth':auth,'form':VoteForm(),'error':u'2 kez oy kullanamzsiniz'})


        vf=VoteForm( { 'vote':request.POST['vote'] } )

        if vf.is_valid():

            fv=vf.cleaned_data['vote']

            if dosya.rate==0:
                dosya.rate=int(fv)
            else:
                dosya.rate=(dosya.rate+int(fv))/2

            try:
                dosya.save()

            except Exception:
                render_to_response('db_error.html')

            request.session[d_id]=True



            return render_to_response('tema/detail.html', {'dosya':dosya,'auth':auth,'form':VoteForm()})

    return render_to_response('404.html')

#end of voting sheyisi

