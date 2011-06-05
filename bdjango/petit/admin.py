from django.contrib import admin
from bdjango.petit.models import Blog, Image, Album, Guestbook, Page, GalleryUpload, Video, VideoComment, ImageComment, BlogComment

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

class VideoAdmin(admin.ModelAdmin):
	list_display = ('id','title','date')
	search_fields = ('id','title','embed_code')

class CommentAdmin(admin.ModelAdmin):
	list_display = ('id','name','comment','date','ip')
	search_fields = ('id','name','comment','ip')

class VideoCommentAdmin(CommentAdmin):
	list_display = ('id','name','comment','date','ip','video')

class ImageCommentAdmin(CommentAdmin):
	list_display = ('id','name','comment','date','ip','image')

class BlogCommentAdmin(CommentAdmin):
	list_display = ('id','name','comment','date','ip','blog')

class GuestbookAdmin(admin.ModelAdmin):
	list_display = ('id','author','date','text','display','ip')
	search_fields = ('id','author','text','ip')

class BlogAdmin(admin.ModelAdmin):
	list_display = ('id','title','author','date','display')
	search_fields = ('id','title','text')

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
admin.site.register(VideoComment, VideoCommentAdmin)
admin.site.register(ImageComment, ImageCommentAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
