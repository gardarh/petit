from django.conf.urls.defaults import *

urlpatterns = patterns('names.views',
    (r'^(\w+)/$', 'names'),
	(r'^(\w+)/view/$', 'names',{'do_view':True}),
	(r'^(\w+)/compare/$', 'compare'),
	)
