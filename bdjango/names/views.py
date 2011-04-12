import json, random
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from forms import CompareForm
import settings
import utils

def names(request,person,do_view=False):
	names = set(json.loads(open(settings.NAMES_DB,'r').read())['names'])
	oked, vetoed = utils.get_data(person)

	if request.method == "POST":
		if 'yes' in request.POST:
			oked.add(request.POST['name'])
		if 'no' in request.POST:
			vetoed.add(request.POST['name'])
		utils.write_data(person, oked, vetoed)
		return HttpResponseRedirect('/names/%s/' % (person,))

	remaining = names - vetoed - oked

	context = {
			'name': random.choice(list(remaining)) if len(remaining) else None
			, 'num_remaining': len(remaining)
			, 'num_ok': len(oked)
			, 'num_veto': len(vetoed)
			}
	if do_view:
		context.update({'do_view':True, 'oked': sorted(list(oked)) , 'vetoed': sorted(list(vetoed))})

	template = 'names/%s.html' % ('namelist' if do_view else 'names',)
	return HttpResponse(loader.get_template(template).render(RequestContext(request,context)))

def compare(request,p1):
	compare_form = CompareForm(request.GET if request.GET.get('submit',None) else None)
	context = {'compare_form':compare_form}
	if compare_form.is_valid():
		p2 = compare_form.cleaned_data['compare_to']
		p1oked, p1vetoed = utils.get_data(p1)
		p2oked, p2vetoed = utils.get_data(p2)
		context['person1'] = p1
		context['person2'] = p2
		context['p1oked'] = utils.sort_nameset(p1oked-p2oked)
		context['p2oked'] = utils.sort_nameset(p2oked-p1oked)
		context['intersection'] = utils.sort_nameset(p2oked.intersection(p1oked))

	return HttpResponse(loader.get_template("names/compare.html").render(RequestContext(request,context)))
