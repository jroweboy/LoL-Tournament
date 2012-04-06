# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Summoner'
        db.create_table('summoners', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('summoner', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('in_queue', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('lan_wins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('played_today', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('lol_tourney', ['Summoner'])

        # Adding model 'Team'
        db.create_table('teams', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('outcome', self.gf('django.db.models.fields.CharField')(default='incomplete', max_length=32)),
        ))
        db.send_create_signal('lol_tourney', ['Team'])

        # Adding M2M table for field players on 'Team'
        db.create_table('teams_players', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm['lol_tourney.team'], null=False)),
            ('summoner', models.ForeignKey(orm['lol_tourney.summoner'], null=False))
        ))
        db.create_unique('teams_players', ['team_id', 'summoner_id'])

        # Adding model 'Match'
        db.create_table('matches', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='blue', to=orm['lol_tourney.Team'])),
            ('purple', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purple', to=orm['lol_tourney.Team'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='display', max_length=32)),
            ('played_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('lol_tourney', ['Match'])


    def backwards(self, orm):
        
        # Deleting model 'Summoner'
        db.delete_table('summoners')

        # Deleting model 'Team'
        db.delete_table('teams')

        # Removing M2M table for field players on 'Team'
        db.delete_table('teams_players')

        # Deleting model 'Match'
        db.delete_table('matches')


    models = {
        'lol_tourney.match': {
            'Meta': {'object_name': 'Match', 'db_table': "'matches'"},
            'blue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blue'", 'to': "orm['lol_tourney.Team']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'played_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'purple': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purple'", 'to': "orm['lol_tourney.Team']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'display'", 'max_length': '32'})
        },
        'lol_tourney.summoner': {
            'Meta': {'object_name': 'Summoner', 'db_table': "'summoners'"},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'icon': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_queue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lan_wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'played_today': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'summoner': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'lol_tourney.team': {
            'Meta': {'object_name': 'Team', 'db_table': "'teams'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome': ('django.db.models.fields.CharField', [], {'default': "'incomplete'", 'max_length': '32'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lol_tourney.Summoner']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['lol_tourney']
