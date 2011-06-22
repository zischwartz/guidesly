# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'StaticElement.length'
        db.add_column('guides_staticelement', 'length', self.gf('django.db.models.fields.TimeField')(default=datetime.date(2011, 6, 20), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'StaticElement.length'
        db.delete_column('guides_staticelement', 'length')


    models = {
        'guides.action': {
            'Meta': {'object_name': 'Action'},
            'goto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Slide']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'play_static': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.StaticElement']", 'null': 'True', 'blank': 'True'}),
            'save_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'guides.conditionalaction': {
            'Meta': {'object_name': 'ConditionalAction', '_ormbases': ['guides.Action']},
            'a_number': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.Action']", 'unique': 'True', 'primary_key': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'guides.guide': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Guide'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_linear': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number_of_slides': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'text_slugs_for_slides': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'guides.interactiveelement': {
            'Meta': {'object_name': 'InteractiveElement'},
            'button_text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'default_action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Action']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Slide']"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        'guides.multiplechoice': {
            'Meta': {'object_name': 'MultipleChoice'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Action']", 'null': 'True', 'blank': 'True'}),
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inquiry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.MultipleChoiceInquiry']"})
        },
        'guides.multiplechoiceinquiry': {
            'Meta': {'object_name': 'MultipleChoiceInquiry', '_ormbases': ['guides.InteractiveElement']},
            'allow_multiple_selections': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'interactiveelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.InteractiveElement']", 'unique': 'True', 'primary_key': 'True'}),
            'show_choices': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'guides.nvalueinquiry': {
            'Meta': {'object_name': 'NValueInquiry', '_ormbases': ['guides.InteractiveElement']},
            'default_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'increment_by': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'interactiveelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.InteractiveElement']", 'unique': 'True', 'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'min_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'guides.slide': {
            'Meta': {'ordering': "['slide_number']", 'object_name': 'Slide'},
            'brand_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'default_next_slide': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['guides.Slide']"}),
            'default_prev_slide': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['guides.Slide']"}),
            'guide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Guide']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alt_slide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slide_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'guides.staticelement': {
            'Meta': {'object_name': 'StaticElement'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_title': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_background': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'length': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'slide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Slide']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        'guides.svalueinquiry': {
            'Meta': {'object_name': 'SValueInquiry', '_ormbases': ['guides.InteractiveElement']},
            'interactiveelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.InteractiveElement']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        'guides.timer': {
            'Meta': {'object_name': 'Timer', '_ormbases': ['guides.InteractiveElement']},
            'execute_action_when_done': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'interactiveelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.InteractiveElement']", 'unique': 'True', 'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seconds': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'guides.tvalueinquiry': {
            'Meta': {'object_name': 'TValueInquiry', '_ormbases': ['guides.InteractiveElement']},
            'default_value': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'interactiveelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.InteractiveElement']", 'unique': 'True', 'primary_key': 'True'})
        },
        'guides.yninquiry': {
            'Meta': {'object_name': 'YNInquiry', '_ormbases': ['guides.InteractiveElement']},
            'interactiveelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.InteractiveElement']", 'unique': 'True', 'primary_key': 'True'}),
            'no_action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'yn_inquiry_no'", 'null': 'True', 'to': "orm['guides.Action']"}),
            'yes_action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'yn_inquiry_yes'", 'null': 'True', 'to': "orm['guides.Action']"})
        }
    }

    complete_apps = ['guides']
