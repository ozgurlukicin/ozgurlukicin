from django.conf.urls.defaults import *

urlpatterns = patterns('oi.ezine.views',
            (r'^$', 'list'),
            (r'^(?P<id>.*)/$', 'detail'),
            )

