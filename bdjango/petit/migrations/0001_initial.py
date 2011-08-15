# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('petit_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('petit', ['Image'])

        # Adding model 'Video'
        db.create_table('petit_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('embed_code', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('petit', ['Video'])

        # Adding model 'Blog'
        db.create_table('petit_blog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('petit', ['Blog'])

        # Adding M2M table for field images on 'Blog'
        db.create_table('petit_blog_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blog', models.ForeignKey(orm['petit.blog'], null=False)),
            ('image', models.ForeignKey(orm['petit.image'], null=False))
        ))
        db.create_unique('petit_blog_images', ['blog_id', 'image_id'])

        # Adding model 'Guestbook'
        db.create_table('petit_guestbook', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal('petit', ['Guestbook'])

        # Adding model 'Album'
        db.create_table('petit_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('display_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='display_image', null=True, to=orm['petit.Image'])),
        ))
        db.send_create_signal('petit', ['Album'])

        # Adding M2M table for field images on 'Album'
        db.create_table('petit_album_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm['petit.album'], null=False)),
            ('image', models.ForeignKey(orm['petit.image'], null=False))
        ))
        db.create_unique('petit_album_images', ['album_id', 'image_id'])

        # Adding model 'Page'
        db.create_table('petit_page', (
            ('heading', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=64, primary_key=True, db_index=True)),
            ('display_link', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('petit', ['Page'])

        # Adding model 'GalleryUpload'
        db.create_table('petit_galleryupload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zip_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['petit.Album'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
        ))
        db.send_create_signal('petit', ['GalleryUpload'])

        # Adding model 'ImageComment'
        db.create_table('petit_imagecomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['petit.Image'])),
        ))
        db.send_create_signal('petit', ['ImageComment'])

        # Adding model 'BlogComment'
        db.create_table('petit_blogcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['petit.Blog'])),
        ))
        db.send_create_signal('petit', ['BlogComment'])

        # Adding model 'VideoComment'
        db.create_table('petit_videocomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['petit.Video'])),
        ))
        db.send_create_signal('petit', ['VideoComment'])


    def backwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('petit_image')

        # Deleting model 'Video'
        db.delete_table('petit_video')

        # Deleting model 'Blog'
        db.delete_table('petit_blog')

        # Removing M2M table for field images on 'Blog'
        db.delete_table('petit_blog_images')

        # Deleting model 'Guestbook'
        db.delete_table('petit_guestbook')

        # Deleting model 'Album'
        db.delete_table('petit_album')

        # Removing M2M table for field images on 'Album'
        db.delete_table('petit_album_images')

        # Deleting model 'Page'
        db.delete_table('petit_page')

        # Deleting model 'GalleryUpload'
        db.delete_table('petit_galleryupload')

        # Deleting model 'ImageComment'
        db.delete_table('petit_imagecomment')

        # Deleting model 'BlogComment'
        db.delete_table('petit_blogcomment')

        # Deleting model 'VideoComment'
        db.delete_table('petit_videocomment')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'petit.album': {
            'Meta': {'ordering': "['date', 'id']", 'object_name': 'Album'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'display_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'display_image'", 'null': 'True', 'to': "orm['petit.Image']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['petit.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'petit.blog': {
            'Meta': {'ordering': "['date']", 'object_name': 'Blog'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['petit.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'petit.blogcomment': {
            'Meta': {'ordering': "['date']", 'object_name': 'BlogComment'},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['petit.Blog']"}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'petit.galleryupload': {
            'Meta': {'object_name': 'GalleryUpload'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['petit.Album']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'zip_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'petit.guestbook': {
            'Meta': {'ordering': "['date']", 'object_name': 'Guestbook'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'petit.image': {
            'Meta': {'ordering': "['date_taken', 'id']", 'object_name': 'Image'},
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'petit.imagecomment': {
            'Meta': {'ordering': "['date']", 'object_name': 'ImageComment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['petit.Image']"}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'petit.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display_link': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'primary_key': 'True', 'db_index': 'True'})
        },
        'petit.video': {
            'Meta': {'object_name': 'Video'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'embed_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'petit.videocomment': {
            'Meta': {'ordering': "['date']", 'object_name': 'VideoComment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['petit.Video']"})
        }
    }

    complete_apps = ['petit']
