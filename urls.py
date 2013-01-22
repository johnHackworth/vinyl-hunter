from django.conf.urls import patterns, include, url
import lastFmUser.urls
import user_session.urls
import artist.urls

urlpatterns = patterns('',
    url(r'lastfm/', include(lastFmUser.urls)),
    url(r'user/', include(user_session.urls)),
    url(r'artist/', include(artist.urls)),
)
