# Generated by Django 2.0.6 on 2018-09-18 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_pages_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='ymap',
            field=models.TextField(blank=True, null=True, verbose_name='Карта'),
        ),
    ]
