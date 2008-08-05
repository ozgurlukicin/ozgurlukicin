from django.conf.urls.defaults import *

urlpatterns = patterns('oi.ideas.views',
    (r'^$', 'list'),
    (r'^ekle$', 'add'),
    (r'^ayrinti/(?P<idea_slug>.*)/new/$', 'new_comment'),
    (r'^ayrinti/(?P<slug>.*)/$', 'detail'),
    (r'^(?P<field>.*)/(?P<filter_slug>.*)/$', 'list' ),

)
