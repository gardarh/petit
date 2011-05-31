from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import settings
from django.utils.translation import ugettext_lazy as _

import Image as PyImage
import zipfile, os, datetime
from cStringIO import StringIO
from utils import EXIF

ORIENTATIONS = {
	1:0
	, 2:0
	, 3:180
	, 4:0
	, 5:90
	, 6:270
	, 7:270
	, 8:90
}

class Image(models.Model):
	title = models.CharField(max_length=256,null=True,blank=True)
	image = models.ImageField(upload_to='uploaded')
	text = models.TextField(null=True,blank=True)
	date_taken = models.DateTimeField(null=True,blank=True)

	def generate_images(self):
		orientation_key = self.EXIF.get('Image Orientation', None)
		im = PyImage.open(self.image.path)
		if orientation_key:
			rotation = ORIENTATIONS.get(orientation_key.values[0],0)
			if rotation != 0:
				im = im.rotate(rotation)
		# im.format gives image format
		width, height = im.size
		ratio = float(width)/float(height)
		img_dimensions = [width, height]
		if width > height:
			# landscape image
			thumb_dimensions = [settings.GALLERY_THUMB_MAX_DIMENSION, int(settings.GALLERY_THUMB_MAX_DIMENSION/ratio)]
			if width > settings.GALLERY_IMG_MAX_DIMENSION:
				img_dimensions = [settings.GALLERY_IMG_MAX_DIMENSION, int(settings.GALLERY_IMG_MAX_DIMENSION/ratio)]
		else:
			# portrait image
			thumb_dimensions = [int(settings.GALLERY_THUMB_MAX_DIMENSION*ratio), settings.GALLERY_THUMB_MAX_DIMENSION]
			if height > settings.GALLERY_IMG_MAX_DIMENSION:
				img_dimensions = [int(settings.GALLERY_IMG_MAX_DIMENSION*ratio), settings.GALLERY_IMG_MAX_DIMENSION]

		im.resize(img_dimensions, PyImage.ANTIALIAS).save(self.get_img_path('img'))
		im.resize(thumb_dimensions, PyImage.ANTIALIAS).save(self.get_img_path('thumb'))

	def get_img_url(self):
		return '/%s/%s' % (settings.GALLERY_DIR, self.get_img_location('img'))

	def get_thumb_url(self):
		return '/%s/%s' % (settings.GALLERY_DIR, self.get_img_location('thumb'))

	def get_img_path(self, imgtype):
		return '%s/%s/%s' % (settings.MEDIA_ROOT, settings.GALLERY_DIR, self.get_img_location(imgtype))

	def get_img_location(self, imgtype):
		if imgtype not in ('img','thumb'): raise ValueError("Invalid imgtype: %s" % (imgtype,))
		return '%s/%07d-%s.jpg' % (settings.GALLERY_IMAGE_PATH if imgtype == 'img' else settings.GALLERY_THUMBNAIL_PATH, self.id, imgtype)

	def __unicode__(self):
		return '%s (%s)' % (self.title, self.date_taken)

	class Meta:
		ordering = ['date_taken','id']

	@property
	def EXIF(self):
		try:
			return EXIF.process_file(open(self.image.path, 'rb'))
		except Exception, e:
			print "EXIF EXP 1",str(e)
			try:
				return EXIF.process_file(open(self.image.path, 'rb'), details=False)
			except Exception, ee:
				print "EXIF EXP 2",str(ee)
				return {}

	def save(self, *args, **kwargs):
		generate_images = kwargs.pop('generate_images',True)
		clean_dict = {}
		if not self.date_taken or True:
			exif_date = self.EXIF.get('EXIF DateTimeOriginal', None)
			if exif_date:
				self.date_taken = datetime.datetime.strptime(exif_date.values,'%Y:%m:%d %H:%M:%S')
			else:
				self.date_taken = datetime.datetime.now()
		super(Image, self).save(*args, **kwargs)
		# Post-save hook: Create album image and thumbnail - original is stored as django wants to
		if generate_images:
			self.generate_images()

class ImageComment(models.Model):
	name = models.CharField(max_length=256)
	comment = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	image = models.ForeignKey(Image)
	ip = models.IPAddressField()

	class Meta:
		ordering = ['date']

class Blog(models.Model):
	author = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=256)
	text = models.TextField()
	display = models.BooleanField(default=True)
	images = models.ManyToManyField(Image,blank=True)

	def __unicode__(self):
		return '%s (%s)' % (self.title,self.date)

	class Meta:
		ordering = ['date']

class Guestbook(models.Model):
	author = models.CharField(max_length=256)
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField(_("Message"))
	display = models.BooleanField(default=True)

	def __unicode__(self):
		return '%s (%s)' % (self.author,self.date)

	class Meta:
		ordering = ['date']

class Album(models.Model):
	title = models.CharField(max_length=256,null=True,blank=True)
	text = models.TextField(null=True,blank=True)
	images = models.ManyToManyField(Image,blank=True)
	date = models.DateTimeField(null=True,blank=True)
	display = models.BooleanField(default=True)
	display_image = models.ForeignKey(Image,related_name='display_image',null=True,blank=True)

	class Meta:
		ordering = ['date']

	def next_image(self, image):
		img_ids = [img.id for img in self.images.all()]
		cur_index = img_ids.index(image.id)
		return Image.objects.get(id=img_ids[cur_index+1]) if cur_index < len(img_ids)-1 else None

	def previous_image(self, image):
		img_ids = [img.id for img in self.images.all()]
		cur_index = img_ids.index(image.id)
		return Image.objects.get(id=img_ids[cur_index-1]) if cur_index > 0 else None

	def __unicode__(self):
		return '%s (%s)' % (self.title, self.date)

class Page(models.Model):
	heading = models.CharField(max_length=64)
	slug = models.SlugField(max_length=64,primary_key=True)
	content = models.TextField(blank=True)

	def __unicode__(self):
		return '%s' % (self.heading,)

class GalleryUpload(models.Model):
	zip_file = models.FileField(_('images file (.zip)'), upload_to='%s/%s/tmp/' % (settings.MEDIA_ROOT, settings.GALLERY_DIR),
								help_text=_('Select a .zip file of images to upload into a new Gallery.'))
	album = models.ForeignKey(Album, null=True, blank=True, help_text=_('Select a album to add these images to. Leave this empty to create a new album from the supplied title.'))
	title = models.CharField(_('title'), max_length=75, help_text=_('All photos in the gallery will be given a title made up of the gallery title + a sequential number.'))
	caption = models.TextField(_('caption'), blank=True, help_text=_('Caption will be added to all photos.'))
	description = models.TextField(_('description'), blank=True, help_text=_('A description of this Gallery.'))
	is_public = models.BooleanField(_('is public'), default=True, help_text=_('Uncheck this to make the uploaded gallery and included photographs private.'))
	#tags = models.CharField(max_length=255, blank=True, verbose_name=_('tags'))

	class Meta:
		verbose_name = _('gallery upload')
		verbose_name_plural = _('gallery uploads')

	def save(self, *args, **kwargs):
		super(GalleryUpload, self).save(*args, **kwargs)
		self.process_zipfile()
		super(GalleryUpload, self).delete()
		return self.album

	def process_zipfile(self):
		if os.path.isfile(self.zip_file.path):
			# TODO: implement try-except here
			zipf = zipfile.ZipFile(self.zip_file.path)
			bad_file = zipf.testzip()
			if bad_file:
				raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
			count = 1
			if not self.album:
				self.album = Album(title=self.title, date=datetime.datetime.now())
				self.album.save()
			for filename in sorted(zipf.namelist()):
				if filename.startswith('__'): # do not process meta files
					continue
				data = zipf.read(filename)
				if len(data):
					try:
						# the following is taken from django.newforms.fields.ImageField:
						#  load() is the only method that can spot a truncated JPEG,
						#  but it cannot be called sanely after verify()
						trial_image = PyImage.open(StringIO(data))
						trial_image.load()
						# verify() is the only method that can spot a corrupt PNG,
						#  but it must be called immediately after the constructor
						trial_image = PyImage.open(StringIO(data))
						trial_image.verify()
					except Exception, e:
						# if a "bad" file is found we just skip it.
						continue
					# TODO:detect img date taken via exif
					img = Image(title='', text='',date_taken=datetime.datetime.now())
					img.image.save(filename, ContentFile(data))
					img.save()
					self.album.images.add(img)
			zipf.close()
