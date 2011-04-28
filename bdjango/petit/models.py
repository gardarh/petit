from django.db import models
from django.contrib.auth.models import User
import settings
import Image as PyImage

class Image(models.Model):
	title = models.CharField(max_length=256,null=True,blank=True)
	image = models.ImageField(upload_to='uploaded')
	text = models.TextField(null=True,blank=True)
	date = models.DateTimeField(null=True,blank=True)

	def save(self):
		# Post-save hook: Create album image and thumbnail - original is stored as django wants to
		super(Image, self).save()
		self.generate_images()
	
	def generate_images(self):
		#print type(self.image),dir(self.image)
		im = PyImage.open(self.image.path)
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
		return '%s (%s)' % (self.title, self.date)

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
	text = models.TextField()
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
	display_image = models.ForeignKey(Image,related_name='display_image')

	class Meta:
		ordering = ['date']

	def __unicode__(self):
		return '%s (%s)' % (self.title, self.date)

class Page(models.Model):
	heading = models.CharField(max_length=64)
	slug = models.SlugField(max_length=64,primary_key=True)
	content = models.TextField(blank=True)

	def __unicode__(self):
		return '%s' % (self.heading,)
