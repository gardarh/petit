import json, random, datetime, urllib
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from forms import CompareForm
import settings
import utils

def names(request,person,do_view=False):
	names = set(json.loads(open(settings.NAMES_DB,'r').read())['names'])
	oked, vetoed = utils.get_data(person)

	if request.method == "POST":
		name = request.POST['name']
		ok = 0
		if 'yes' in request.POST:
			oked.add(name)
			ok = 1
		if 'no' in request.POST:
			vetoed.add(name)
		if 'cancel' in request.POST:
			if name in oked:
				oked.remove(name)
			if name in vetoed:
				vetoed.remove(name)
		utils.write_data(person, oked, vetoed)
		response = HttpResponseRedirect('/names/%s/' % (person,))
		if 'yes' in request.POST or 'no' in request.POST:
			safe_name = urllib.quote(name.encode('UTF-8'))
			response.set_cookie('last_decision',value='%s|%s' % (ok,safe_name),max_age=60*60) 
		return response

	remaining = names - vetoed - oked

	last_decision = request.COOKIES.get('last_decision','|').split('|')
	last_decision[1] = urllib.unquote(last_decision[1])
	context = {
			'name': random.choice(list(remaining)) if len(remaining) else None
			, 'num_remaining': len(remaining)
			, 'num_ok': len(oked)
			, 'num_veto': len(vetoed)
			, 'last_decision': last_decision
			}
	if do_view:
		context.update({'do_view':True, 'oked': utils.sort_nameset(oked) , 'vetoed': utils.sort_nameset(vetoed)})

	template = 'names/%s.html' % ('namelist' if do_view else 'names',)
	response = HttpResponse(loader.get_template(template).render(RequestContext(request,context)))
	response.delete_cookie('last_decision')
	return response

def compare(request,p1):
	compare_form = CompareForm(request.GET if request.GET.get('submit',None) else None)
	context = {'compare_form':compare_form,'person1':p1}
	if compare_form.is_valid():
		p2 = compare_form.cleaned_data['compare_to']
		p1oked, p1vetoed = utils.get_data(p1)
		p2oked, p2vetoed = utils.get_data(p2)
		context['person2'] = p2
		context['p1oked'] = utils.sort_nameset(p1oked-p2oked)
		context['p2oked'] = utils.sort_nameset(p2oked-p1oked)
		context['intersection'] = utils.sort_nameset(p2oked.intersection(p1oked))

	return HttpResponse(loader.get_template("names/compare.html").render(RequestContext(request,context)))
