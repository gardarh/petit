from django.contrib import admin
from bdjango.petit.models import Blog, Image, Album, Guestbook, Page, GalleryUpload

class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug":('heading',)}

class GalleryUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False # To remove the 'Save and continue editing' button

admin.site.register(Guestbook)
admin.site.register(Blog)
admin.site.register(Image)
admin.site.register(Album)
admin.site.register(Page, PageAdmin)
admin.site.register(GalleryUpload, GalleryUploadAdmin)
