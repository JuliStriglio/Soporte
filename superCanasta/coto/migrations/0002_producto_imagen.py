# Generated by Django 5.0.6 on 2024-10-23 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.URLField(default=0),
            preserve_default=False,
        ),
    ]
