from django.conf.urls.defaults import *

urlpatterns = patterns('oi.flatpages.views', (r'^(?P<url>.*)$', 'flatpage'),)