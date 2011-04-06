from django.conf.urls.defaults import *
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^img/(.*)$','django.views.static.serve', {'document_root': '%s%s' % (settings.MEDIA_ROOT, 'img')}),
    (r'^js/(.*)$','django.views.static.serve',  {'document_root': '%s%s' % (settings.MEDIA_ROOT, 'js')}),
    (r'^css/(.*)$','django.views.static.serve',  {'document_root': '%s%s' % (settings.MEDIA_ROOT, 'css')}),
    (r'^uploaded/(.*)$','django.views.static.serve',  {'document_root': '%s%s' % (settings.MEDIA_ROOT, 'uploaded')}),

    (r'login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/'}),
)

urlpatterns += patterns('petit.views',
    (r'^$', 'frontpage'),
	)
