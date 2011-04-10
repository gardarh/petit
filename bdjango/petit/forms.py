from django import forms
from models import Guestbook
from django.utils.translation import ugettext_lazy as _

class GuestbookForm(forms.ModelForm):
	class Meta:
		model = Guestbook
		exclude = ['date','display']

class PasswordForm(forms.Form):
	password = forms.CharField(_("Password"), widget=forms.widgets.PasswordInput)
