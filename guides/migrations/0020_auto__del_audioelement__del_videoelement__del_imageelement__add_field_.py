# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'AudioElement'
        db.delete_table('guides_audioelement')

        # Deleting model 'VideoElement'
        db.delete_table('guides_videoelement')

        # Deleting model 'ImageElement'
        db.delete_table('guides_imageelement')

        # Adding field 'Guide.has_title_slide'
        db.add_column('guides_guide', 'has_title_slide', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'StaticElement.is_background'
        db.add_column('guides_staticelement', 'is_background', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'StaticElement.autoplay'
        db.add_column('guides_staticelement', 'autoplay', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'StaticElement.length_seconds'
        db.add_column('guides_staticelement', 'length_seconds', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'StaticElement.length_minutes'
        db.add_column('guides_staticelement', 'length_minutes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Changing field 'StaticElement.type'
        db.alter_column('guides_staticelement', 'type', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Deleting field 'ConditionalAction.action_ptr'
        db.delete_column('guides_conditionalaction', 'action_ptr_id')

        # Deleting field 'ConditionalAction.a_number'
        db.delete_column('guides_conditionalaction', 'a_number')

        # Adding field 'ConditionalAction.id'
        db.add_column('guides_conditionalaction', 'id', self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True), keep_default=False)

        # Adding field 'ConditionalAction.text__match_answer'
        db.add_column('guides_conditionalaction', 'text__match_answer', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True), keep_default=False)

        # Adding field 'ConditionalAction.b_number'
        db.add_column('guides_conditionalaction', 'b_number', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'ConditionalAction.goto'
        db.add_column('guides_conditionalaction', 'goto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Slide'], null=True, blank=True), keep_default=False)

        # Adding field 'ConditionalAction.save_choice'
        db.add_column('guides_conditionalaction', 'save_choice', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'ConditionalAction.play_static'
        db.add_column('guides_conditionalaction', 'play_static', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.StaticElement'], null=True, blank=True), keep_default=False)

        # Changing field 'ConditionalAction.condition'
        db.alter_column('guides_conditionalaction', 'condition', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))


    def backwards(self, orm):
        
        # Adding model 'AudioElement'
        db.create_table('guides_audioelement', (
            ('staticelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.StaticElement'], unique=True, primary_key=True)),
            ('length_minutes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('continue_playing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('length_seconds', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('autoplay', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('guides', ['AudioElement'])

        # Adding model 'VideoElement'
        db.create_table('guides_videoelement', (
            ('length_minutes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('staticelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.StaticElement'], unique=True, primary_key=True)),
            ('length_seconds', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('autoplay', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('guides', ['VideoElement'])

        # Adding model 'ImageElement'
        db.create_table('guides_imageelement', (
            ('is_background', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('staticelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.StaticElement'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('guides', ['ImageElement'])

        # Deleting field 'Guide.has_title_slide'
        db.delete_column('guides_guide', 'has_title_slide')

        # Deleting field 'StaticElement.is_background'
        db.delete_column('guides_staticelement', 'is_background')

        # Deleting field 'StaticElement.autoplay'
        db.delete_column('guides_staticelement', 'autoplay')

        # Deleting field 'StaticElement.length_seconds'
        db.delete_column('guides_staticelement', 'length_seconds')

        # Deleting field 'StaticElement.length_minutes'
        db.delete_column('guides_staticelement', 'length_minutes')

        # Changing field 'StaticElement.type'
        db.alter_column('guides_staticelement', 'type', self.gf('django.db.models.fields.CharField')(max_length=1))

        # Adding field 'ConditionalAction.action_ptr'
        db.add_column('guides_conditionalaction', 'action_ptr', self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['guides.Action'], unique=True, primary_key=True), keep_default=False)

        # Adding field 'ConditionalAction.a_number'
        db.add_column('guides_conditionalaction', 'a_number', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Deleting field 'ConditionalAction.id'
        db.delete_column('guides_conditionalaction', 'id')

        # Deleting field 'ConditionalAction.text__match_answer'
        db.delete_column('guides_conditionalaction', 'text__match_answer')

        # Deleting field 'ConditionalAction.b_number'
        db.delete_column('guides_conditionalaction', 'b_number')

        # Deleting field 'ConditionalAction.goto'
        db.delete_column('guides_conditionalaction', 'goto_id')

        # Deleting field 'ConditionalAction.save_choice'
        db.delete_column('guides_conditionalaction', 'save_choice')

        # Deleting field 'ConditionalAction.play_static'
        db.delete_column('guides_conditionalaction', 'play_static_id')

        # User chose to not deal with backwards NULL issues for 'ConditionalAction.condition'
        raise RuntimeError("Cannot reverse this migration. 'ConditionalAction.condition' and its values cannot be restored.")


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
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '150', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        },
        'guides.action': {
            'Meta': {'object_name': 'Action'},
            'goto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Slide']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'play_static': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.StaticElement']", 'null': 'True', 'blank': 'True'}),
            'save_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'guides.conditionalaction': {
            'Meta': {'object_name': 'ConditionalAction'},
            'b_number': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'goto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Slide']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'play_static': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.StaticElement']", 'null': 'True', 'blank': 'True'}),
            'save_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text__match_answer': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'guides.guide': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Guide'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_title_slide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_linear': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number_of_slides': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '250', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
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
            'autoplay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_title': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.UserFile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_background': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'length_minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'length_seconds': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Slide']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
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
