from django.contrib import admin
from bdjango.petit.models import Blog, Image, Album, Guestbook

admin.site.register(Guestbook)
admin.site.register(Blog)
admin.site.register(Image)
admin.site.register(Album)
