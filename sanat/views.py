# Create your views here.
from django.views.generic.list_detail import object_list
from sanat_settings import HOME_ITEMS
from oi.sanat.models import Dosya,Category 
from django.shortcuts import render_to_response,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.comments.views.comments import post_free_comment
from django.http import HttpResponseRedirect

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
                'template_name':'sanat/main.html',
                    
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
                'template_name':'sanat/main.html',
                    
                    }
					
	return object_list(request,**params)
        

def file_detail(request,file_id):
	"""" Shows the details of the file"""
	
	#we know it is a int
	dosya = get_object_or_404(Dosya, pk=file_id)
	
	dosya.counter +=1
	dosya.save()
	
	
	return render_to_response('sanat/detail.html', {'dosya':dosya})

	
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
                'template_name':'sanat/main.html',
                    
                    }
					
	return object_list(request,**params)
    

def add_file(request):
	""" That one will add a file to the system the hardest one !"""
	pass

def my_post_free_comment(request):
	""" Comment wrapper for free comments"""
	if request.has_key('url') and not request.has_key('preview'):
		response = post_free_comment(request)
		# ensure there's a url to redirect to, and that post_free_comment worked
		if len(request['url'].strip()) > 0 and isinstance(response, HttpResponseRedirect):
			return redirect_to(request, request['url'])
		# fallback on the default post_free_comment response
		return response
	return post_free_comment(request)
