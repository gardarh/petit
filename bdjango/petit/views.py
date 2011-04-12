from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from models import Blog, Guestbook, Image
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
			}
	return HttpResponse(loader.get_template("login.html").render(RequestContext(request,context)))

def logout(request):
	response = HttpResponseRedirect(settings.SITE_LOGIN_URL)
	response.delete_cookie('password')
	return response

@password_protect
def frontpage(request):
	blogs = Blog.objects.filter(display=True).order_by('date')[0:10]

	context = {
			'blogs': blogs
			}
	return HttpResponse(loader.get_template("frontpage.html").render(RequestContext(request,context)))

@password_protect
def blog(request):
	blogs = Blog.objects.filter(display=True).order_by('date')

	context = {
			'blogs': blogs
			}
	return HttpResponse(loader.get_template("blog.html").render(RequestContext(request,context)))


@password_protect
def guestbook(request):
	entries = Guestbook.objects.filter(display=True).order_by('date')[0:20]

	context = {
			'entries': entries
			}
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

def images(request, image_id):
	image = Image.objects.get(id=int(image_id))

	context = {
			'image': image
			}
	return HttpResponse(loader.get_template("image.html").render(RequestContext(request,context)))
