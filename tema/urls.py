from django.conf.urls.defaults import *
from oi.tema.feeds import *

feed_dict = {
             'rss': Tema_RSS,
             'atom': Tema_Atom,
            }

cat_feed_dict = {
             'rss': Category_Tema_Rss,
             'atom': Category_Tema_Atom,
            }

user_feed_dict = {
             'rss': User_Tema_Rss,
             'atom': User_Tema_Atom,
            }

urlpatterns = patterns ('oi.tema.views',
        #the first page listing
        (r'^goster/(?P<sort_by>(son|begenilen|indirilen))/$','themeitem_list'),
        (r'^kategori/(?P<category>[a-z-]+)/$','list_category'),
        (r'^dosya/(?P<item_id>[0-9]+)/$','themeitem_detail'),
        (r'^kullanici/(?P<username>[a-z]+)/$','list_user'),
        (r'^oyla/(?P<item_id>[0-9]+)/(?P<rating>[0-4])/$','vote'),
        (r'^ekle/$','themeitem_create'),
)

urlpatterns+=patterns('',
        #the rss feeds
        #(r'^feed/(?P<url>.*)/yeni/$', 'django.contrib.syndication.views.feed', {'feed_dict': feed_dict}),
        (r'^feed/kategori/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': cat_feed_dict}),
        (r'^feed/kullanici/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': user_feed_dict}),
)
