from django import template
register = template.Library()

@register.filter
def addint(string, addition):
	return '%s%s' % (string, addition)

@register.filter
def loadvars(string):
	# returns a list of tuples, parsed from a key,var;key,var
	return [item.split(',') for item in string.split(';')] if string else []
