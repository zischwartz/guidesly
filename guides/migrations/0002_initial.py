# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Theme'
        db.create_table('guides_theme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('guides', ['Theme'])

        # Adding model 'Guide'
        db.create_table('guides_guide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from=None, unique_with=(), db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_linear', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('enable_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('text_slugs_for_cards', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('card_order', self.gf('jsonfield.fields.JSONField')(default='[]', blank=True)),
            ('floating_list', self.gf('jsonfield.fields.JSONField')(default='[]', blank=True)),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Theme'], null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('show_toc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('first_card', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['guides.Card'])),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('private_url', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('thumb', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fileupload.UserFile'], null=True, blank=True)),
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
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=500, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=None, db_index=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('guide', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Guide'], null=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('card_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('primary_media', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='primary_media', null=True, blank=True, to=orm['guides.MediaElement'])),
            ('is_floating_card', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Theme'], null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('autoplay', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('primary_is_bg', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_lots_of_text', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_next', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_prev', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('guides', ['Card'])

        # Adding model 'CommentCard'
        db.create_table('guides_commentcard', (
            ('card_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.Card'], unique=True, primary_key=True)),
            ('parent_card', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child_comment_card', null=True, to=orm['guides.Card'])),
            ('parent_comment_card', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='comments_child_comment_card', null=True, to=orm['guides.CommentCard'])),
        ))
        db.send_create_signal('guides', ['CommentCard'])

        # Adding model 'MediaElement'
        db.create_table('guides_mediaelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=250, null=True, blank=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Card'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fileupload.UserFile'], null=True)),
            ('external_file', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('action_when_complete', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.Action'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['MediaElement'])

        # Adding model 'Action'
        db.create_table('guides_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('goto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Card'], null=True, blank=True)),
            ('goto_guide', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Guide'], null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['Action'])

        # Adding model 'Condition'
        db.create_table('guides_condition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.Action'], unique=True, null=True, blank=True)),
            ('input', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.InputElement'])),
        ))
        db.send_create_signal('guides', ['Condition'])

        # Adding model 'MapPointElement'
        db.create_table('guides_mappointelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('point', self.gf('django.db.models.fields.IntegerField')(max_length=500)),
            ('point_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('manual_addy', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('default_action', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.Action'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('guides', ['MapPointElement'])

        # Adding model 'MapElement'
        db.create_table('guides_mapelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Card'])),
            ('map_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(default='map', max_length=100)),
        ))
        db.send_create_signal('guides', ['MapElement'])

        # Adding M2M table for field points on 'MapElement'
        db.create_table('guides_mapelement_points', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mapelement', models.ForeignKey(orm['guides.mapelement'], null=False)),
            ('mappointelement', models.ForeignKey(orm['guides.mappointelement'], null=False))
        ))
        db.create_unique('guides_mapelement_points', ['mapelement_id', 'mappointelement_id'])

        # Adding model 'InputElement'
        db.create_table('guides_inputelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guides.Card'])),
            ('button_text', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('sub_title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('default_action', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['guides.Action'], unique=True, null=True, blank=True)),
            ('big', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seconds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('minutes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('execute_action_when_done', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ding_when_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auto_start', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_match_message', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('should_save_answer', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('guides', ['InputElement'])


    def backwards(self, orm):
        
        # Deleting model 'Theme'
        db.delete_table('guides_theme')

        # Deleting model 'Guide'
        db.delete_table('guides_guide')

        # Removing M2M table for field cards on 'Guide'
        db.delete_table('guides_guide_cards')

        # Deleting model 'Card'
        db.delete_table('guides_card')

        # Deleting model 'CommentCard'
        db.delete_table('guides_commentcard')

        # Deleting model 'MediaElement'
        db.delete_table('guides_mediaelement')

        # Deleting model 'Action'
        db.delete_table('guides_action')

        # Deleting model 'Condition'
        db.delete_table('guides_condition')

        # Deleting model 'MapPointElement'
        db.delete_table('guides_mappointelement')

        # Deleting model 'MapElement'
        db.delete_table('guides_mapelement')

        # Removing M2M table for field points on 'MapElement'
        db.delete_table('guides_mapelement_points')

        # Deleting model 'InputElement'
        db.delete_table('guides_inputelement')


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
        'fileupload.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'fileupload.userfile': {
            'Meta': {'ordering': "['-created']", 'object_name': 'UserFile'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'display_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.Image']", 'null': 'True', 'blank': 'True'}),
            'medium_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '150', 'blank': 'True'}),
            'thumb_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        },
        'guides.action': {
            'Meta': {'object_name': 'Action'},
            'goto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Card']", 'null': 'True', 'blank': 'True'}),
            'goto_guide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Guide']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'guides.card': {
            'Meta': {'ordering': "['is_floating_card', 'card_number']", 'object_name': 'Card'},
            'autoplay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'card_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'guide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Guide']", 'null': 'True'}),
            'has_lots_of_text': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_floating_card': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'primary_is_bg': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'primary_media': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'primary_media'", 'null': 'True', 'blank': 'True', 'to': "orm['guides.MediaElement']"}),
            'show_next': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_prev': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Theme']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'guides.commentcard': {
            'Meta': {'ordering': "['is_floating_card', 'card_number']", 'object_name': 'CommentCard', '_ormbases': ['guides.Card']},
            'card_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.Card']", 'unique': 'True', 'primary_key': 'True'}),
            'parent_card': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_comment_card'", 'null': 'True', 'to': "orm['guides.Card']"}),
            'parent_comment_card': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comments_child_comment_card'", 'null': 'True', 'to': "orm['guides.CommentCard']"})
        },
        'guides.condition': {
            'Meta': {'object_name': 'Condition'},
            'action': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.Action']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.InputElement']"}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'guides.guide': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Guide'},
            'card_order': ('jsonfield.fields.JSONField', [], {'default': "'[]'", 'blank': 'True'}),
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'cards_in_guide'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['guides.Card']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_card': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['guides.Card']"}),
            'floating_list': ('jsonfield.fields.JSONField', [], {'default': "'[]'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_linear': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'private_url': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_toc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'text_slugs_for_cards': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Theme']", 'null': 'True', 'blank': 'True'}),
            'thumb': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.UserFile']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'guides.inputelement': {
            'Meta': {'object_name': 'InputElement'},
            'auto_start': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'big': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'button_text': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Card']"}),
            'default_action': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.Action']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'ding_when_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'execute_action_when_done': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'no_match_message': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'seconds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'should_save_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'})
        },
        'guides.mapelement': {
            'Meta': {'object_name': 'MapElement'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'points': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['guides.MapPointElement']", 'symmetrical': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'map'", 'max_length': '100'})
        },
        'guides.mappointelement': {
            'Meta': {'object_name': 'MapPointElement'},
            'default_action': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.Action']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_addy': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'point': ('django.db.models.fields.IntegerField', [], {'max_length': '500'}),
            'point_title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'guides.mediaelement': {
            'Meta': {'object_name': 'MediaElement'},
            'action_when_complete': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['guides.Action']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guides.Card']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'external_file': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.UserFile']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        },
        'guides.theme': {
            'Meta': {'object_name': 'Theme'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['guides']
