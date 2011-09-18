import settings
from models import Page, StyleSheetSection

def site_config(request):
	link_pages = Page.objects.filter(display_link=True)

	return {
			'site_title':settings.SITE_TITLE
			, 'link_pages': link_pages
			, 'styles': '\n'.join([sss.content for sss in StyleSheetSection.objects.filter(enable=True)])
			}
