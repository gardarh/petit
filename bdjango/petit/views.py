import urllib
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import Blog, Guestbook, Image, Album, Page, Video, VideoComment, ImageComment, BlogComment
from forms import GuestbookForm, PasswordForm, ImageSettingsForm, VideoCommentForm, ImageCommentForm, BlogCommentForm
from decorators import password_protect
import settings

def login(request):
	password_form = PasswordForm()

	if request.method == "POST":
		password_form = PasswordForm(request.POST)
		if password_form.is_valid() and password_form.cleaned_data['password'] == settings.SITE_PASSWORD:
			response = HttpResponseRedirect('/')
			response.set_cookie('password', value=password_form.cleaned_data['password'], max_age=60*60*24*60) # 60 days
			return response
	context = {
			'password_form': password_form
			, 'hide_sidebar': True
			}
	return HttpResponse(loader.get_template("login.html").render(RequestContext(request,context)))

def logout(request):
	response = HttpResponseRedirect(settings.SITE_LOGIN_URL)
	response.delete_cookie('password')
	return response

@password_protect
def page(request,slug):
	context = {'page': Page.objects.get(slug=slug)}
	return HttpResponse(loader.get_template("page.html").render(RequestContext(request,context)))

@password_protect
def diary(request):
	comment_instance = BlogComment(ip=request.META.get('HTTP_X_REAL_IP',request.META['REMOTE_ADDR']),name=request.COOKIES.get('comment_name',None))
	comment_form = BlogCommentForm(instance=comment_instance, data=request.POST if request.method == "POST" and 'submit_comment' in request.POST else None)
	if request.method == "POST" and 'submit_comment' in request.POST and comment_form.is_valid():
		comment_instance.blog = Blog.objects.get(id=int(request.POST['blog_id']))
		comment = comment_form.save()
		
		messages.success(request, _("Comment added"))
		response = HttpResponseRedirect('/diary/')
		response.set_cookie('comment_name', value=comment_form.cleaned_data['name'].encode("UTF-8"), max_age=60*60*24*100)
		return response
	context = {
			'blogs': Blog.objects.filter(display=True).order_by('-date')
			, 'comment_form': comment_form
			}
	return HttpResponse(loader.get_template("blog.html").render(RequestContext(request,context)))

@password_protect
def guestbook(request):
	instance = Guestbook(display=True,ip=request.META.get('HTTP_X_REAL_IP',request.META['REMOTE_ADDR']))
	guestbook_form = GuestbookForm(instance=instance)
	start_at = max(int(request.GET.get('start_at','0')),0)
	items_per_page = 20

	if request.method == "POST":
		guestbook_form = GuestbookForm(request.POST, instance=instance)
		if guestbook_form.is_valid():
			guestbook_form.save(request)
			messages.success(request, _("Guestbook entry added"))
			return HttpResponseRedirect('/guestbook/')


	context = {
			'guestbook_form': guestbook_form
			, 'entries': Guestbook.objects.filter(display=True).order_by('-date')[start_at:start_at+items_per_page]
			, 'display_next_page':len(Guestbook.objects.filter(display=True).order_by('-date')[start_at+items_per_page:]) > 0
			, 'display_last_page':start_at>0
			, 'next_startat':start_at+items_per_page
			, 'last_startat':max(start_at-items_per_page,0)
			}
	return HttpResponse(loader.get_template("guestbook.html").render(RequestContext(request,context)))

@password_protect
def images(request, image_id):
	context = { 'image': Image.objects.get(id=int(image_id)) }
	return HttpResponse(loader.get_template("image.html").render(RequestContext(request,context)))

@password_protect
def videos(request):
	comment_instance = VideoComment(ip=request.META.get('HTTP_X_REAL_IP',request.META['REMOTE_ADDR']),name=request.COOKIES.get('comment_name',None))
	comment_form = VideoCommentForm(instance=comment_instance, data=request.POST if request.method == "POST" and 'submit_comment' in request.POST else None)
	if request.method == "POST" and 'submit_comment' in request.POST and comment_form.is_valid():
		comment_instance.video = Video.objects.get(id=int(request.POST['video_id']))
		comment = comment_form.save()
		messages.success(request, _("Comment added"))
		response = HttpResponseRedirect('/videos/')
		response.set_cookie('comment_name', value=comment_form.cleaned_data['name'].encode("UTF-8"), max_age=60*60*24*100)
		return response
	context = {
			'videos': Video.objects.all().order_by('-date')
			, 'comment_form': comment_form
			}
	return HttpResponse(loader.get_template("videos.html").render(RequestContext(request,context)))

@password_protect
def albums(request,album_id=None):
	context = { 'albums': Album.objects.all().order_by('-date') }
	return HttpResponse(loader.get_template("albums.html").render(RequestContext(request,context)))

@password_protect
def album(request,album_id):
	context = { 'album': Album.objects.get(id=int(album_id)) }
	return HttpResponse(loader.get_template("album.html").render(RequestContext(request,context)))

@password_protect
def album_image(request,album_id,image_id):

	album = Album.objects.get(id=int(album_id))
	image = Image.objects.get(id=int(image_id), album=album)

	titleform = None
	comment_instance = ImageComment(ip=request.META.get('HTTP_X_REAL_IP',request.META['REMOTE_ADDR']), name=request.COOKIES.get('comment_name',None), image=image)
	comment_form = ImageCommentForm(instance=comment_instance, data=request.POST if request.method == "POST" and 'submit_comment' in request.POST else None)
	if request.method == "POST" and 'submit_comment' in request.POST and comment_form.is_valid():
		comment = comment_form.save()
		messages.success(request, _("Comment added"))
		response = HttpResponseRedirect('/albums/%d/%d' % (album.id, image.id))
		response.set_cookie('comment_name', value=comment_form.cleaned_data['name'].encode("UTF-8"), max_age=60*60*24*100)
		return response

	if request.user.is_authenticated():
		titleform = ImageSettingsForm(image=image, album=album, data=request.POST if request.method == "POST" and 'submit_settings' in request.POST else None)
		if request.method == "POST" and titleform.is_valid() and 'submit_settings' in request.POST:
			titleform.save()
			messages.success(request, _("Title saved"))
			return HttpResponseRedirect('/albums/%d/%d/' % (album.id, image.id))

	context = {
			'album': album
			, 'image': image
			, 'titleform': titleform
			, 'next_image': album.next_image(image)
			, 'previous_image': album.previous_image(image)
			, 'comment_form': comment_form
			, 'img_no': album.cur_image_no(image)
			}
	return HttpResponse(loader.get_template("album_image.html").render(RequestContext(request,context)))

@login_required
def newsfeed(request):
	start_at = max(int(request.GET.get('start_at','0')),0)
	items_per_page = 20
	feed = []
	for classtype in [ImageComment, VideoComment, BlogComment]:
		feed.extend(classtype.objects.all().order_by('-date')[0:start_at+items_per_page])
	feed.sort(key=lambda x:x.date, reverse=True)
	[f.item_url() for f in feed]

	entries = feed[start_at:start_at+items_per_page]
	context = {
			'newsfeed': entries
			, 'display_last_page':start_at>0
			, 'display_next_page':len(entries) == items_per_page
			, 'next_startat':start_at+items_per_page
			, 'last_startat':max(start_at-items_per_page,0)
			}
	return HttpResponse(loader.get_template("newsfeed.html").render(RequestContext(request,context)))
