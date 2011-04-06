from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
	title = models.CharField(max_length=256,null=True,blank=True)
	image = models.ImageField(upload_to='uploaded')
	text = models.TextField(null=True,blank=True)
	date = models.DateTimeField(null=True,blank=True)

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

class Album(models.Model):
	title = models.CharField(max_length=256,null=True,blank=True)
	text = models.TextField(null=True,blank=True)
	images = models.ManyToManyField(Image,blank=True)
	date = models.DateTimeField(null=True,blank=True)

	def __unicode__(self):
		return '%s (%s)' % (self.title, self.date)
