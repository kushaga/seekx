from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


PATH = getattr(settings, 'URL_PATH', '')

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seekx.views.home', name='home'),
    # url(r'^seekx/', include('seekx.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^%s$' % PATH, 'seek.views.home',name='home'),
    url(r'^%slogout$' % PATH, 'seek.views.logout',name='logout'),
    url(r'^%sdone/$' % PATH, 'seek.views.done', name='done'),
    url(r'^%sdashboard/$' % PATH, 'seek.views.dashboard', name='dashboard'),
    url(r'^%screateevent/$' % PATH, 'seek.views.createevent', name='createevent'),
    url(r'^%ssignup/$' % PATH, 'seek.views.signup', name='signup'),
    url(r'^%sprofile/$' % PATH, 'seek.views.profile', name='profile'),
    url(r'^%supdateprofile/$' % PATH, 'seek.views.updateprofile', name='updateprofile'),
    url(r'^%ssendmail/$' % PATH, 'seek.views.sendmail', name='sendmail'),

    url(r'^%sproject/$' % PATH, 'seek.views.project', name='project'),
    url(r'^%smovies/$' % PATH, 'seek.views.movies', name='movies'),
    url(r'^%shangout/$' % PATH, 'seek.views.hangout', name='hangout'),
    url(r'^%sfood/$' % PATH, 'seek.views.food', name='food'),
    url(r'^%scompetitions/$' % PATH, 'seek.views.competitions', name='competitions'),
    url(r'^%smisc/$' % PATH, 'seek.views.misc', name='misc'),
    url(r'^%ssports/$' % PATH, 'seek.views.sports', name='sports'),
    url(r'^%scarpool/$' % PATH, 'seek.views.carpool', name='carpool'),

    url(r'^user/(?P<user_id>\d+)/$', 'seek.views.user', name='user'),
    
    url(r'%s' % PATH, include('social.apps.django_app.urls',
        namespace='social'))
)
