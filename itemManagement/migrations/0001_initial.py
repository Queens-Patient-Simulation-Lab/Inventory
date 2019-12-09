# Generated by Django 2.2.7 on 2019-11-26 05:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kghID', models.CharField(max_length=20, null=True)),
                ('title', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('unit', models.CharField(max_length=20, null=True)),
                ('lastUsed', models.DateTimeField(default=datetime.datetime.now)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('alertThreshold', models.PositiveSmallIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mimeType', models.CharField(max_length=20)),
                ('data', models.CharField(max_length=200)),
                ('order', models.PositiveSmallIntegerField()),
                ('depicts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itemManagement.Item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itemManagement.Item')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itemManagement.Location')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='locations',
            field=models.ManyToManyField(through='itemManagement.ItemStorage', to='itemManagement.Location'),
        ),
    ]