# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Guide'
        db.create_table('guides_guide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_linear', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enable_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('guides', ['Guide'])

        # Adding model 'Slide'
        db.create_table('guides_slide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('guide', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Guide'])),
            ('slide_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_alt_slide', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('guides', ['Slide'])

        # Adding model 'StaticElement'
        db.create_table('guides_staticelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slide', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Slide'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('display_title', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
        ))
        db.send_create_signal('guides', ['StaticElement'])

        # Adding model 'Action'
        db.create_table('guides_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('goto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Slide'], null=True, blank=True)),
            ('save_choice', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('play_static', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.StaticElement'], null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['Action'])

        # Adding model 'ConditionalAction'
        db.create_table('guides_conditionalaction', (
            ('action_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.Action'], unique=True, primary_key=True)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('guides', ['ConditionalAction'])

        # Adding model 'InteractiveElement'
        db.create_table('guides_interactiveelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slide', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Slide'])),
            ('button_text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('default_action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Action'], null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['InteractiveElement'])

        # Adding model 'MultipleChoices'
        db.create_table('guides_multiplechoices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Action'], null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['MultipleChoices'])

        # Adding model 'MultipleChoiceInquiry'
        db.create_table('guides_multiplechoiceinquiry', (
            ('interactiveelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.InteractiveElement'], unique=True, primary_key=True)),
            ('choices', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.MultipleChoices'], null=True, blank=True)),
            ('show_choices', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('guides', ['MultipleChoiceInquiry'])

        # Adding model 'YNInquiry'
        db.create_table('guides_yninquiry', (
            ('interactiveelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.InteractiveElement'], unique=True, primary_key=True)),
            ('yes_action', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='yn_inquiry_yes', null=True, to=orm['guides.Action'])),
            ('no_action', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='yn_inquiry_no', null=True, to=orm['guides.Action'])),
        ))
        db.send_create_signal('guides', ['YNInquiry'])

        # Adding model 'ValueInquiry'
        db.create_table('guides_valueinquiry', (
            ('interactiveelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.InteractiveElement'], unique=True, primary_key=True)),
            ('min_value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['ValueInquiry'])

        # Adding model 'Timer'
        db.create_table('guides_timer', (
            ('interactiveelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.InteractiveElement'], unique=True, primary_key=True)),
            ('seconds', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('minutes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('execute_action_when_done', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('guides', ['Timer'])


    def backwards(self, orm):
        
        # Deleting model 'Guide'
        db.delete_table('guides_guide')

        # Deleting model 'Slide'
        db.delete_table('guides_slide')

        # Deleting model 'StaticElement'
        db.delete_table('guides_staticelement')

        # Deleting model 'Action'
        db.delete_table('guides_action')

        # Deleting model 'ConditionalAction'
        db.delete_table('guides_conditionalaction')

        # Deleting model 'InteractiveElement'
        db.delete_table('guides_interactiveelement')

        # Deleting model 'MultipleChoices'
        db.delete_table('guides_multiplechoices')

        # Deleting model 'MultipleChoiceInquiry'
        db.delete_table('guides_multiplechoiceinquiry')

        # Deleting model 'YNInquiry'
        db.delete_table('guides_yninquiry')

        # Deleting model 'ValueInquiry'
        db.delete_table('guides_valueinquiry')

        # Deleting model 'Timer'
        db.delete_table('guides_timer')


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
            'action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.Action']", 'unique': 'True', 'primary_key': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'guides.guide': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Guide'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_linear': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
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
        'guides.multiplechoiceinquiry': {
            'Meta': {'object_name': 'MultipleChoiceInquiry', '_ormbases': ['guides.InteractiveElement']},
            'choices': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.MultipleChoices']", 'null': 'True', 'blank': 'True'}),
            'interactiveelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.InteractiveElement']", 'unique': 'True', 'primary_key': 'True'}),
            'show_choices': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'guides.multiplechoices': {
            'Meta': {'object_name': 'MultipleChoices'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Action']", 'null': 'True', 'blank': 'True'}),
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'guides.slide': {
            'Meta': {'ordering': "['slide_number']", 'object_name': 'Slide'},
            'guide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Guide']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alt_slide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slide_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'guides.staticelement': {
            'Meta': {'object_name': 'StaticElement'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_title': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Slide']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        'guides.timer': {
            'Meta': {'object_name': 'Timer', '_ormbases': ['guides.InteractiveElement']},
            'execute_action_when_done': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'interactiveelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.InteractiveElement']", 'unique': 'True', 'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seconds': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'guides.valueinquiry': {
            'Meta': {'object_name': 'ValueInquiry', '_ormbases': ['guides.InteractiveElement']},
            'interactiveelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.InteractiveElement']", 'unique': 'True', 'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'guides.yninquiry': {
            'Meta': {'object_name': 'YNInquiry', '_ormbases': ['guides.InteractiveElement']},
            'interactiveelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.InteractiveElement']", 'unique': 'True', 'primary_key': 'True'}),
            'no_action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'yn_inquiry_no'", 'null': 'True', 'to': "orm['guides.Action']"}),
            'yes_action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'yn_inquiry_yes'", 'null': 'True', 'to': "orm['guides.Action']"})
        }
    }

    complete_apps = ['guides']
