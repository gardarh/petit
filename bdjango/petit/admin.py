from django.contrib import admin
from bdjango.petit.models import Blog, Image, Album, Guestbook, Page, GalleryUpload, ImageComment

class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug":('heading',)}

class AlbumAdmin(admin.ModelAdmin):
	filter_horizontal = ('images',)

class GalleryUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False # To remove the 'Save and continue editing' button

admin.site.register(Guestbook)
admin.site.register(Blog)
admin.site.register(Image)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(GalleryUpload, GalleryUploadAdmin)
admin.site.register(ImageComment)
