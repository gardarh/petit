from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from models import Blog, Guestbook, Image, Album, Page
from forms import GuestbookForm, PasswordForm
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
def blog(request):
	context = { 'blogs': Blog.objects.filter(display=True).order_by('date') }
	return HttpResponse(loader.get_template("blog.html").render(RequestContext(request,context)))


@password_protect
def guestbook(request):
	context = { 'entries': Guestbook.objects.filter(display=True).order_by('date')[0:20] }
	return HttpResponse(loader.get_template("guestbook.html").render(RequestContext(request,context)))

@password_protect
def guestbook_form(request):
	instance = Guestbook(display=True)
	guestbook_form = GuestbookForm(instance=instance)

	if request.method == "POST":
		guestbook_form = GuestbookForm(request.POST, instance=instance)
		if guestbook_form.is_valid():
			guestbook_form.save()
			return HttpResponseRedirect('/guestbook/')

	context = {
			'guestbook_form': guestbook_form
			}
	return HttpResponse(loader.get_template("guestbook_form.html").render(RequestContext(request,context)))

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
	image = album.objects.get(id=int(image_id))
	context = { 'album': album, 'image': image }
	return HttpResponse(loader.get_template("album_image.html").render(RequestContext(request,context)))
