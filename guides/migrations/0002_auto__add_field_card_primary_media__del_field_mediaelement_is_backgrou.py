# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Card.primary_media'
        db.add_column('guides_card', 'primary_media', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='primary_media', null=True, to=orm['guides.MediaElement']), keep_default=False)

        # Deleting field 'MediaElement.is_background'
        db.delete_column('guides_mediaelement', 'is_background')

        # Deleting field 'MediaElement.is_primary'
        db.delete_column('guides_mediaelement', 'is_primary')

        # Adding field 'MediaElement.action_when_complete'
        db.add_column('guides_mediaelement', 'action_when_complete', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.Action'], unique=True, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Card.primary_media'
        db.delete_column('guides_card', 'primary_media_id')

        # Adding field 'MediaElement.is_background'
        db.add_column('guides_mediaelement', 'is_background', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'MediaElement.is_primary'
        db.add_column('guides_mediaelement', 'is_primary', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'MediaElement.action_when_complete'
        db.delete_column('guides_mediaelement', 'action_when_complete_id')


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
        'fileupload.userfile': {
            'Meta': {'ordering': "['-created']", 'object_name': 'UserFile'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '150', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        },
        'guides.action': {
            'Meta': {'object_name': 'Action'},
            'goto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Card']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'play_static': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.MediaElement']", 'null': 'True', 'blank': 'True'}),
            'save_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'guides.card': {
            'Meta': {'ordering': "['created']", 'object_name': 'Card'},
            'brand_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'card_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Guide']", 'null': 'True'}),
            'has_lots_of_text': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'primary_media': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary_media'", 'null': 'True', 'to': "orm['guides.MediaElement']"}),
            'representative_media': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'show_last_and_next_buttons': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'guides.conditionalaction': {
            'Meta': {'object_name': 'ConditionalAction'},
            'b_number': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'goto_on_false': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'goto_on_false'", 'null': 'True', 'to': "orm['guides.Card']"}),
            'goto_on_true': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'goto_on_true'", 'null': 'True', 'to': "orm['guides.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'play_static': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.MediaElement']", 'null': 'True', 'blank': 'True'}),
            'save_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text__match_answer': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'guides.guide': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Guide'},
            'card_order': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'cards_in_guide'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['guides.Card']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_title_card': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_linear': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number_of_cards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '250', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'text_slugs_for_cards': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'guides.inputelement': {
            'Meta': {'object_name': 'InputElement'},
            'button_text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Card']"}),
            'default_action': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.Action']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'default_goto': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['guides.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'})
        },
        'guides.mediaelement': {
            'Meta': {'object_name': 'MediaElement'},
            'action_when_complete': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.Action']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'autoplay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Card']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'external_file': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.UserFile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'length_seconds': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        }
    }

    complete_apps = ['guides']
