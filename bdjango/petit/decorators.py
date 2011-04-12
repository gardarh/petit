import settings
from django.http import HttpResponseRedirect
from functools import wraps

def password_protect(view_func):
	@wraps(view_func)
	def decorator(*args, **kwargs):
		request = args[0]
		if request.COOKIES.get('password') != settings.SITE_PASSWORD:
			return HttpResponseRedirect(settings.SITE_LOGIN_URL)
		return view_func(*args, **kwargs)
	return decorator
		
