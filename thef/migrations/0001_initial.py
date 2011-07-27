# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'theF'
        db.create_table('thef_thef', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('the_data', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
        ))
        db.send_create_signal('thef', ['theF'])


    def backwards(self, orm):
        
        # Deleting model 'theF'
        db.delete_table('thef_thef')


    models = {
        'thef.thef': {
            'Meta': {'object_name': 'theF'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'the_data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        }
    }

    complete_apps = ['thef']
