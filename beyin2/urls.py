from django.conf.urls.defaults import *
from django.contrib.auth.views import login
# Uncomment the next two lines to enable the admin:
urlpatterns = patterns('oi.beyin2.views',

    (r'^$', 'index'),
    #url(r'^(?P<blog_id>\d+)/$',"blog_goster",name="blog_goster"),
    #url(r'^(?P<blog_id>\d+)/(?P<yazi_id>\d+)/yorum_ekle/$',"yorum_ekle",name="yorum_ekle"),
)

