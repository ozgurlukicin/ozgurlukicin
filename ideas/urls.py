from django.conf.urls.defaults import *

urlpatterns = patterns('oi.ideas.views',
                       (r'^$', 'list'),
                       (r'^ekle/$', 'add'),
                       (r'^oyla/(?P<idea_id>.*)/(?P<vote>[0,1])/$', 'vote_idea'),
                       (r'^ayrinti/(?P<idea_id>.*)/$', 'detail'),
                       (r'^ayrinti/(?P<idea_id>.*)/favori/ekle$', 'add_favorite'),
                       (r'^ayrinti/(?P<idea_id>.*)/favori/cikar$', 'del_favorite'),
                       (r'^listele/(?P<field>.*)/(?P<filter_slug>.*)/$', 'list'),
                       (r'^oyiptal/(?P<idea_id>.*)/$', 'delete_vote'),
                       (r'^tekrar/(?P<idea_id>.*)/(?P<duplicate_id>.*)/$', 'duplicate'),
)
