# Generated by Django 4.0 on 2021-12-27 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiservice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='child_area_ids',
            field=models.JSONField(default=''),
            preserve_default=False,
        ),
    ]
