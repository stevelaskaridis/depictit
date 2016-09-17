# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 13:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Scoreboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_number', models.IntegerField()),
                ('team_score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='depictit_backend.Player')),
                ('turn', models.IntegerField(default=0)),
                ('no_players', models.IntegerField(default=2)),
            ],
        ),
        migrations.AddField(
            model_name='scoreboard',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depictit_backend.Game'),
        ),
    ]