from django.contrib import admin
from bdjango.petit.models import Blog, Image, Album, Guestbook, Page, GalleryUpload, Comment, Video

class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug":('heading',)}
	list_display = ('slug','heading','display_link')
	search_fields = ('slug','heading','content')

class AlbumAdmin(admin.ModelAdmin):
	list_display = ('id','title','text','date','num_images')
	filter_horizontal = ('images',)

class ImageAdmin(admin.ModelAdmin):
	list_display = ('id','title','date_taken','in_albums')
	search_fields = ('id','title','album__id','album__title')
	filter_horizontal = ('comments',)

class VideoAdmin(admin.ModelAdmin):
	list_display = ('id','title','date')
	search_fields = ('id','title','embed_code')
	filter_horizontal = ('comments',)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('id','name','comment','date','ip')
	search_fields = ('id','name','comment','ip')

class GuestbookAdmin(admin.ModelAdmin):
	list_display = ('id','author','date','text','display','ip')
	search_fields = ('id','author','text','ip')

class BlogAdmin(admin.ModelAdmin):
	list_display = ('id','title','author','date','display')
	search_fields = ('id','title','text')
	filter_horizontal = ('comments',)

class GalleryUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False # To remove the 'Save and continue editing' button

admin.site.register(Guestbook, GuestbookAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(GalleryUpload, GalleryUploadAdmin)
admin.site.register(Comment, CommentAdmin)
