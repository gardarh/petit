import urllib
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import Blog, Guestbook, Image, Album, Page, ImageComment
from forms import GuestbookForm, PasswordForm, ImageSettingsForm, ImageCommentForm
from decorators import password_protect
import settings

def login(request):
	password_form = PasswordForm()

	if request.method == "POST":
		password_form = PasswordForm(request.POST)
		if password_form.is_valid() and password_form.cleaned_data['password'] == settings.SITE_PASSWORD:
			response = HttpResponseRedirect('/')
			response.set_cookie('password', value=password_form.cleaned_data['password'])
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
def page(request,slug,hide_heading=False):
	context = {'page': Page.objects.get(slug=slug), 'hide_heading': hide_heading}
	return HttpResponse(loader.get_template("page.html").render(RequestContext(request,context)))

@password_protect
def diary(request):
	context = { 'blogs': Blog.objects.filter(display=True).order_by('date') }
	return HttpResponse(loader.get_template("blog.html").render(RequestContext(request,context)))


@password_protect
def guestbook(request):
	instance = Guestbook(display=True)
	guestbook_form = GuestbookForm(instance=instance)

	if request.method == "POST":
		guestbook_form = GuestbookForm(request.POST, instance=instance)
		if guestbook_form.is_valid():
			guestbook_form.save()
			messages.success(request, _("Guestbook entry added"))
			return HttpResponseRedirect('/guestbook/')

	context = {
			'guestbook_form': guestbook_form
			, 'entries': Guestbook.objects.filter(display=True).order_by('date')[0:20]
			}
	return HttpResponse(loader.get_template("guestbook.html").render(RequestContext(request,context)))

@password_protect
def images(request, image_id):
	context = { 'image': Image.objects.get(id=int(image_id)) }
	return HttpResponse(loader.get_template("image.html").render(RequestContext(request,context)))

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
	comment_instance = ImageComment(image=image,ip=request.META['REMOTE_ADDR'],name=request.COOKIES.get('comment_name',None))
	comment_form = ImageCommentForm(instance=comment_instance, data=request.POST if request.method == "POST" and 'submit_comment' in request.POST else None)
	if request.method == "POST" and 'submit_comment' in request.POST and comment_form.is_valid():
		comment_form.save()
		messages.success(request, _("Comment added"))
		response = HttpResponseRedirect('/albums/%d/%d' % (album.id, image.id))
		response.set_cookie('comment_name', value=comment_form.cleaned_data['name'].encode("UTF-8"), max_age=60*60*24*100)
		return response

	if request.user.is_authenticated():
		titleform = ImageSettingsForm(image=image, album=album, data=request.POST if request.method == "POST" and 'submit_settings' in request.POST else None)
		if request.method == "POST" and titleform.is_valid() and 'submit_settings' in request.POST:
			titleform.save()
			messages.success(request, _("Title saved"))
			return HttpResponseRedirect('/albums/%d/%d' % (album.id, image.id))

	context = {
			'album': album
			, 'image': image
			, 'titleform': titleform
			, 'next_image': album.next_image(image)
			, 'previous_image': album.previous_image(image)
			, 'comment_form': comment_form
			}
	return HttpResponse(loader.get_template("album_image.html").render(RequestContext(request,context)))
