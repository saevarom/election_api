# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 19:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0003_auto_20161021_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('voters', models.IntegerField()),
                ('available_seats', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ElectionResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votes', models.IntegerField()),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Election')),
            ],
        ),
        migrations.CreateModel(
            name='ElectoralList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('constituency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Constituency')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Election')),
            ],
        ),
        migrations.CreateModel(
            name='ElectoralListSeat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.IntegerField()),
                ('electoral_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ElectoralList')),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=10)),
                ('logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.OvercastImage')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.OvercastImage')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Election')),
            ],
        ),
        migrations.CreateModel(
            name='PollResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votes', models.IntegerField()),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Party')),
            ],
        ),
        migrations.AddField(
            model_name='electorallist',
            name='party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Party'),
        ),
        migrations.AddField(
            model_name='electionresult',
            name='party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Party'),
        ),
        migrations.AddField(
            model_name='constituency',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Election'),
        ),
    ]
