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
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=250, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_linear', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enable_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('text_slugs_for_cards', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('number_of_cards', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('has_title_card', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('card_order', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['Guide'])

        # Adding M2M table for field cards on 'Guide'
        db.create_table('guides_guide_cards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('guide', models.ForeignKey(orm['guides.guide'], null=False)),
            ('card', models.ForeignKey(orm['guides.card'], null=False))
        ))
        db.create_unique('guides_guide_cards', ['guide_id', 'card_id'])

        # Adding model 'Card'
        db.create_table('guides_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('guide', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Guide'], null=True)),
            ('brand_new', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lots_of_text', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal('guides', ['Card'])

        # Adding model 'StaticElement'
        db.create_table('guides_staticelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Card'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_background', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('autoplay', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('length_seconds', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('length_minutes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fileupload.UserFile'])),
            ('external_file', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('guides', ['StaticElement'])

        # Adding model 'Action'
        db.create_table('guides_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('goto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Card'], null=True, blank=True)),
            ('save_choice', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('play_static', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.StaticElement'], null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['Action'])

        # Adding model 'ConditionalAction'
        db.create_table('guides_conditionalaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('text__match_answer', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('b_number', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('goto_on_true', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='goto_on_true', null=True, to=orm['guides.Card'])),
            ('goto_on_false', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='goto_on_false', null=True, to=orm['guides.Card'])),
            ('save_choice', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('play_static', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.StaticElement'], null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['ConditionalAction'])

        # Adding model 'InteractiveElement'
        db.create_table('guides_interactiveelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Card'])),
            ('button_text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('default_action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Action'], null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['InteractiveElement'])

        # Adding model 'MultipleChoiceInquiry'
        db.create_table('guides_multiplechoiceinquiry', (
            ('interactiveelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.InteractiveElement'], unique=True, primary_key=True)),
            ('show_choices', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_multiple_selections', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('guides', ['MultipleChoiceInquiry'])

        # Adding model 'MultipleChoice'
        db.create_table('guides_multiplechoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Action'], null=True, blank=True)),
            ('inquiry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.MultipleChoiceInquiry'])),
        ))
        db.send_create_signal('guides', ['MultipleChoice'])

        # Adding model 'NValueInquiry'
        db.create_table('guides_nvalueinquiry', (
            ('interactiveelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.InteractiveElement'], unique=True, primary_key=True)),
            ('min_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('max_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('increment_by', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('default_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['NValueInquiry'])

        # Adding model 'TValueInquiry'
        db.create_table('guides_tvalueinquiry', (
            ('interactiveelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.InteractiveElement'], unique=True, primary_key=True)),
            ('default_value', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['TValueInquiry'])

        # Adding model 'SValueInquiry'
        db.create_table('guides_svalueinquiry', (
            ('interactiveelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.InteractiveElement'], unique=True, primary_key=True)),
            ('sensor_type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
        ))
        db.send_create_signal('guides', ['SValueInquiry'])

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

        # Removing M2M table for field cards on 'Guide'
        db.delete_table('guides_guide_cards')

        # Deleting model 'Card'
        db.delete_table('guides_card')

        # Deleting model 'StaticElement'
        db.delete_table('guides_staticelement')

        # Deleting model 'Action'
        db.delete_table('guides_action')

        # Deleting model 'ConditionalAction'
        db.delete_table('guides_conditionalaction')

        # Deleting model 'InteractiveElement'
        db.delete_table('guides_interactiveelement')

        # Deleting model 'MultipleChoiceInquiry'
        db.delete_table('guides_multiplechoiceinquiry')

        # Deleting model 'MultipleChoice'
        db.delete_table('guides_multiplechoice')

        # Deleting model 'NValueInquiry'
        db.delete_table('guides_nvalueinquiry')

        # Deleting model 'TValueInquiry'
        db.delete_table('guides_tvalueinquiry')

        # Deleting model 'SValueInquiry'
        db.delete_table('guides_svalueinquiry')

        # Deleting model 'Timer'
        db.delete_table('guides_timer')


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
            'goto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Card']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'play_static': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.StaticElement']", 'null': 'True', 'blank': 'True'}),
            'save_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'guides.card': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Card'},
            'brand_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Guide']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lots_of_text': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'guides.conditionalaction': {
            'Meta': {'object_name': 'ConditionalAction'},
            'b_number': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'goto_on_false': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'goto_on_false'", 'null': 'True', 'to': "orm['guides.Card']"}),
            'goto_on_true': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'goto_on_true'", 'null': 'True', 'to': "orm['guides.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'play_static': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.StaticElement']", 'null': 'True', 'blank': 'True'}),
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
            'number_of_cards': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '250', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'text_slugs_for_cards': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'guides.interactiveelement': {
            'Meta': {'object_name': 'InteractiveElement'},
            'button_text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Card']"}),
            'default_action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Action']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        'guides.staticelement': {
            'Meta': {'object_name': 'StaticElement'},
            'autoplay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Card']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'external_file': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.UserFile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_background': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'length_minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'length_seconds': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['guides']
