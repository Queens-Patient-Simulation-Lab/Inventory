# Generated by Django 2.2.7 on 2020-02-26 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import logs.models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_auto_20200225_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlogs',
            name='logCode',
            field=models.CharField(max_length=1024, validators=[logs.models.validate_notNone]),
        ),
        migrations.AlterField(
            model_name='userlogs',
            name='logMsg',
            field=models.CharField(max_length=1024, validators=[logs.models.validate_notNone]),
        ),
        migrations.AlterField(
            model_name='userlogs',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now, validators=[logs.models.validate_notNone]),
        ),
        migrations.AlterField(
            model_name='userlogs',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operator', to=settings.AUTH_USER_MODEL, validators=[logs.models.validate_notNone]),
        ),
    ]
