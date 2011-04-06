from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from models import Blog

def frontpage(request):
	blogs = Blog.objects.filter(display=True).order_by('date')[0:10]

	context = {
			'blogs': blogs
			}
	return HttpResponse(loader.get_template("frontpage.html").render(RequestContext(request,context)))
