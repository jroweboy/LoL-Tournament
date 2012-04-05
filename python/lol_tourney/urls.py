from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('lol_tourney.views',
    # Examples:
    #url(r'^about/$', 'about', name='About'),
    #url(r'^matches/$', 'matches', name='Current Matches'),
    url(r'^queue/$', 'queue'),
    url(r'^matchmake/$', 'matchmake'),
)
