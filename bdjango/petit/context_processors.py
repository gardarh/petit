import settings

def site_config(request):
	return {'site_title':settings.SITE_TITLE}
