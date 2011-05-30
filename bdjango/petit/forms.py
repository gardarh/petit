from django import forms
from models import Guestbook, ImageComment
from django.utils.translation import ugettext_lazy as _

class GuestbookForm(forms.ModelForm):
	class Meta:
		model = Guestbook
		exclude = ['date','display']

class PasswordForm(forms.Form):
	password = forms.CharField(_("Password"), widget=forms.widgets.PasswordInput)

class ImageTitleForm(forms.Form):
	title = forms.CharField(_("Title"),required=False)

	def __init__(self, *args, **kwargs):
		self.instance = kwargs.pop('instance')
		super(ImageTitleForm, self).__init__(*args, **kwargs)
		self.fields['title'].initial = self.instance.title


	def save(self):
		self.instance.title = self.cleaned_data['title']
		self.instance.save(generate_images=False)

class ImageCommentForm(forms.ModelForm):
	class Meta:
		fields = ['name','comment']
		model = ImageComment
