from django.conf.urls.defaults import *

urlpatterns = patterns('oi.ideas.views',
                       (r'^oyla/(?P<idea_id>.*)/(?P<vote>[0,1])/$', 'vote_idea'),
                       (r'^$', 'list'),
                       (r'^ekle/$', 'add'),
                       (r'^ayrinti/(?P<idea_id>.*)/$', 'detail'),
                       (r'^listele/(?P<field>.*)/(?P<filter_slug>.*)/$', 'list'),

)
