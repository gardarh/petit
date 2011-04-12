import os.path, json, locale
import settings

def get_data(person):
	answersfile = '%s/%s.json' % (settings.DATADIR,person)
	vetoed = set()
	oked = set()
	if os.path.isfile(answersfile):
		json_dict = json.loads(open(answersfile,'r').read())
		vetoed = set(json_dict['vetoed'])
		oked = set(json_dict['oked'])
	return oked, vetoed

def write_data(person, oked, vetoed):
	answersfile = '%s/%s.json' % (settings.DATADIR,person)
	f = open(answersfile,'w')
	f.write(json.dumps({'vetoed':list(vetoed),'oked':list(oked)}))
	f.close()

def sort_nameset(nameset):
	return sorted(list(nameset), cmp=locale.strcoll)
