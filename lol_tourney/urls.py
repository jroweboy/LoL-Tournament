from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('lol_tourney.views',
    # Examples:
    #url(r'^about/$', 'about', name='About'),
    #url(r'^matches/$', 'matches', name='Current Matches'),
    url(r'^$', 'home', name='home'),
    url(r'^queue/$', 'queue'),
    url(r'^matchmake/$', 'matchmake'),
    url(r'^finishMatch/$', 'finishMatch'),
    url(r'^accounts/userinfo/$', 'user_info'),
    url(r'^joinQueue/$', 'join_queue'),
    url(r'^ajax/updateQueue$', 'ajaxUpdateQueue'),
    url(r'^ajax/updateMatch$', 'ajaxUpdateMatches'),
    url(r'^ajax/kickMatch$', 'kick_match'),
)


urlpatterns += patterns('django.contrib.auth.views',
    url(r'^accounts/login/', 'login', {'template_name': 'registration/login.html'}),
    url(r'^accounts/logout/', 'logout', {'template_name': 'registration/logout.html'}),
    url(r'^accounts/password/reset/$', 'password_reset', {'post_reset_redirect' : '/accounts/password/reset/done/'}),
    url(r'^accounts/password/reset/done/$', 'password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm', 
        {'post_reset_redirect' : '/accounts/password/done/'}),
    url(r'^accounts/password/done/$', 'password_reset_complete'),
)
