from django.contrib import admin
from bdjango.petit.models import Blog, Image, Album, Guestbook, Page

admin.site.register(Guestbook)
admin.site.register(Blog)
admin.site.register(Image)
admin.site.register(Album)
class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug":('heading',)}
admin.site.register(Page, PageAdmin)
