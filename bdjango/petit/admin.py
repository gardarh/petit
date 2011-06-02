from django.contrib import admin
from bdjango.petit.models import Blog, Image, Album, Guestbook, Page, GalleryUpload, ImageComment

class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug":('heading',)}

class AlbumAdmin(admin.ModelAdmin):
	list_display = ('id','title','text','date','num_images')
	filter_horizontal = ('images',)

class ImageAdmin(admin.ModelAdmin):
	list_display = ('id','title','date_taken')
	search_fields = ('id','title','album__id','album__title')

class ImageCommentAdmin(admin.ModelAdmin):
	list_display = ('id','name','comment','date','ip','image')
	search_fields = ('id','name','comment','ip','image__id')

class GuestbookAdmin(admin.ModelAdmin):
	list_display = ('id','author','date','text','display','ip')
	search_fields = ('id','author','text','ip')

class GalleryUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False # To remove the 'Save and continue editing' button

admin.site.register(Guestbook, GuestbookAdmin)
admin.site.register(Blog)
admin.site.register(Image, ImageAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(GalleryUpload, GalleryUploadAdmin)
admin.site.register(ImageComment, ImageCommentAdmin)
