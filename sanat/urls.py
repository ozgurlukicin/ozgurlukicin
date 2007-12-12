from django.conf.urls.defaults import *


urlpatterns = patterns ('oi.sanat.views',
	 					#the first page listing
						(r'^goster/(?P<sort_by>[a-z]+)/$','list_material'),
						(r'^kategori/(?P<cat_name>)[a-z]+/$','list_category'),
		  				(r'^dosya/(?P<file_id>)[0-9]+/$','file_detail'),
)
