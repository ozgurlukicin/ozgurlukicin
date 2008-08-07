from django.conf.urls.defaults import *

urlpatterns = patterns('oi.ideas.views',
                       (r'^oyla/(?P<idea_id>.*)/(?P<vote>.\d)/$', 'vote_idea'),
                       (r'^$', 'list'),
                       (r'^ekle/$', 'add'),

                       (r'^ayrinti/(?P<slug>.*)/$', 'detail'),
                       (r'^(?P<field>.*)/(?P<filter_slug>.*)/$', 'list'),

)
