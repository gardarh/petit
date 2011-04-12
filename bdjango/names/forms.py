from django import forms

class CompareForm(forms.Form):
	compare_to = forms.CharField()
