from django.conf.urls.defaults import *
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
	(r'^photologue/', include('photologue.urls')),

    (r'^img/(.*)$','django.views.static.serve', {'document_root': '%s%s' % (settings.MEDIA_ROOT, 'img')}),
    (r'^js/(.*)$','django.views.static.serve',  {'document_root': '%s%s' % (settings.MEDIA_ROOT, 'js')}),
    (r'^css/(.*)$','django.views.static.serve',  {'document_root': '%s%s' % (settings.MEDIA_ROOT, 'css')}),
    (r'^uploaded/(.*)$','django.views.static.serve',  {'document_root': '%s%s' % (settings.MEDIA_ROOT, 'uploaded')}),

)

urlpatterns += patterns('petit.views',
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),

    (r'^$', 'frontpage'),
    (r'^blog/$', 'blog'),
    (r'^guestbook/$', 'guestbook'),
    (r'^guestbook/add/$', 'guestbook_form'),
    (r'^names/$', 'names'),


	)