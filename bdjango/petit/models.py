from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import settings
from django.utils.translation import ugettext_lazy as _

import zipfile, os, datetime, collections
import Image as PyImage
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

		im.resize(img_dimensions, PyImage.ANTIALIAS).convert("RGB").save(self.get_img_path('img'),"JPEG",quality=90)
		im.resize(thumb_dimensions, PyImage.ANTIALIAS).convert("RGB").save(self.get_img_path('thumb'),"JPEG",quality=90)

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
		return '%d: %s' % (self.id, self.title,)

	def in_albums(self):
		return ', '.join([a.title for a in self.album_set.all()])

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
		date_from_image = kwargs.pop('date_from_image',False)
		clean_dict = {}
		if not self.date_taken or date_from_image:
			exif_date = self.EXIF.get('EXIF DateTimeOriginal', None)
			if exif_date:
				self.date_taken = datetime.datetime.strptime(exif_date.values,'%Y:%m:%d %H:%M:%S')
			else:
				self.date_taken = datetime.datetime.now()
		super(Image, self).save(*args, **kwargs)
		# Post-save hook: Create album image and thumbnail - original is stored as django wants to
		if generate_images:
			self.generate_images()

class Video(models.Model):
	title = models.CharField(max_length=256)
	date = models.DateTimeField()
	embed_code = models.TextField(blank=True)

	def __unicode__(self):
		return '%d: %s' % (self.id, self.title,)

class Blog(models.Model):
	author = models.ForeignKey(User)
	date = models.DateTimeField()
	title = models.CharField(max_length=256)
	text = models.TextField()
	display = models.BooleanField(default=True)
	images = models.ManyToManyField(Image,blank=True)

	def __unicode__(self):
		return '%d: %s' % (self.id, self.title)

	class Meta:
		ordering = ['date']

class Guestbook(models.Model):
	author = models.CharField(verbose_name=_("Name"), max_length=256)
	date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
	text = models.TextField(verbose_name=_("Message"))
	display = models.BooleanField(verbose_name=_("Display"), default=True)
	ip = models.IPAddressField(verbose_name=_("IP Address"))

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
		ordering = ['date','id']

	def cur_image_no(self, image):
		img_ids = [img.id for img in self.images.all()]
		return img_ids.index(image.id) + 1

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

	def date_range(self):
		return collections.namedtuple('DateRange',['begins','ends'])(self.images.all()[0].date_taken, self.images.latest('date_taken').date_taken) if self.images.count() > 0 else None

	def num_images(self):
		return self.images.count()

	def save(self, *args, **kwargs):
		if self.id:
			daterange = self.date_range()
			if not self.date and daterange:
				self.date = daterange.ends
		return super(Album, self).save(*args, **kwargs)

class Page(models.Model):
	heading = models.CharField(max_length=64,blank=True)
	slug = models.SlugField(max_length=64,primary_key=True)
	display_link = models.BooleanField()
	content = models.TextField(blank=True)

	def __unicode__(self):
		return '%s' % (self.heading,)

class GalleryUpload(models.Model):
	zip_file = models.FileField(verbose_name=_('images file (.zip)'), upload_to='%s/%s/tmp/' % (settings.MEDIA_ROOT, settings.GALLERY_DIR),
								help_text=_('Select a .zip file of images to upload into a new Gallery.'))
	album = models.ForeignKey(Album, verbose_name=_("album"), null=True, blank=True, help_text=_('Select a album to add these images to. Leave this empty to create a new album from the supplied title.'))
	title = models.CharField(verbose_name=_('title'), max_length=75, help_text=_('If no album is provided above you must enter a title.'), blank=True)

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
					img = Image(title='', text='',date_taken=datetime.datetime.now())
					img.image.save(filename, ContentFile(data))
					img.save(date_from_image=True)
					self.album.images.add(img)
			zipf.close()

class Comment(models.Model):
	name = models.CharField(verbose_name=_("Name"), max_length=256)
	comment = models.TextField(verbose_name=_("Comment"))
	date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
	ip = models.IPAddressField(verbose_name=_("IP Address"))

	def item(self):
		raise NotImplementedError()

	def item_type(self):
		raise NotImplementedError()

	def item_title(self):
		raise NotImplementedError()

	def item_url(self):
		raise NotImplementedError()

	class Meta:
		ordering = ['date']
		abstract = True

	def __unicode__(self):
		return "%s by %s at %s" % (self.comment, self.name, self.date.strftime("%Y-%m-%d"))

class ImageComment(Comment):
	image = models.ForeignKey(Image)

	def item(self):
		return self.image

	def item_type(self):
		return _('theimage')

	def item_title(self):
		return self.image.title

	def item_url(self):
		try:
			return '/albums/%d/%d' % (self.image.album_set.latest('date').id, self.image.id)
		except Album.DoesNotExist:
			return None

class BlogComment(Comment):
	blog = models.ForeignKey(Blog)

	def item(self):
		return self.blog

	def item_type(self):
		return _('theblog')

	def item_title(self):
		return self.blog.title

	def item_url(self):
		# Hmmm, nothing special here
		return '/diary/'

class VideoComment(Comment):
	video = models.ForeignKey(Video)

	def item(self):
		return self.video

	def item_type(self):
		return _('thevideo')

	def item_title(self):
		return self.video.title

	def item_url(self):
		# Hmmm, nothing special here
		return '/videos/'

class StyleSheetSection(models.Model):
	name = models.CharField(max_length=255)
	content = models.TextField(blank=True)
	enable = models.BooleanField()
