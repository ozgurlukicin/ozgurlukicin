from django.conf.urls.defaults import *

urlpatterns = patterns('oi.ideas.views',
                       (r'^$', 'list'),
                       (r'^ekle/$', 'add'),
                       (r'^duzenle/(?P<idea_id>.*)/$', 'edit_idea'),
                       (r'^sil/(?P<idea_id>.*)/$', 'delete_idea'),
                       (r'^oyla/$', 'vote'),
                       (r'^ayrinti/(?P<idea_id>.*)/$', 'detail'),
                       (r'^ayrinti/(?P<idea_id>.*)/favori/ekle$', 'add_favorite'),
                       (r'^ayrinti/(?P<idea_id>.*)/favori/cikar$', 'del_favorite'),
                       (r'^listele/(?P<field>.*)/(?P<filter_slug>.*)/$', 'list'),
                       (r'^tekrar/(?P<idea_id>.*)/(?P<duplicate_id>.*)/$', 'duplicate'),
                       (r'^durumdegistir/((?P<idea_id>.*))/(?P<new_status>.*)/$', 'change_status'),
)
