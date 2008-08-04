from django.conf.urls.defaults import *

urlpatterns = patterns('oi.ideas.views',
    (r'^$', 'list'),
    (r'^ayrinti/(?P<slug>.*)/$', 'detail'),
    (r'^(?P<field>.*)/(?P<filter_slug>.*)/$', 'list' ),
)
