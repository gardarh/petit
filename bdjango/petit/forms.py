from django import forms
from models import Guestbook, ImageComment
from django.utils.translation import ugettext_lazy as _

class GuestbookForm(forms.ModelForm):
	class Meta:
		model = Guestbook
		exclude = ['date','display','ip']

class PasswordForm(forms.Form):
	password = forms.CharField(_("Password"), widget=forms.widgets.PasswordInput)

class ImageSettingsForm(forms.Form):
	title = forms.CharField(_("Title"),required=False)
	use_on_album_overview = forms.BooleanField(required=False)

	def __init__(self, *args, **kwargs):
		self.image = kwargs.pop('image')
		self.album = kwargs.pop('album')
		super(ImageSettingsForm, self).__init__(*args, **kwargs)
		self.fields['title'].initial = self.image.title
		self.fields['use_on_album_overview'].initial = True if self.album.display_image == self.image else False

	def save(self):
		self.image.title = self.cleaned_data['title']
		if self.cleaned_data['use_on_album_overview']:
			self.album.display_image = self.image
			self.album.save()
		self.image.save(generate_images=False)

class ImageCommentForm(forms.ModelForm):
	class Meta:
		fields = ['name','comment']
		model = ImageComment
