from django.conf.urls import patterns, include, url
import lastFmUser.urls

urlpatterns = patterns('',
    url(r'^lastfm/', include(lastFmUser.urls)),
    # Examples:
    # url(r'^$', 'vinylhunter.views.home', name='home'),
    # url(r'^vinylhunter/', include('vinylhunter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
