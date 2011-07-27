# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'theF.the_data_text'
        db.add_column('thef_thef', 'the_data_text', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'theF.the_data_text'
        db.delete_column('thef_thef', 'the_data_text')


    models = {
        'thef.thef': {
            'Meta': {'object_name': 'theF'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'the_data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'the_data_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        }
    }

    complete_apps = ['thef']
