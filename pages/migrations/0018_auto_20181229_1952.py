# Generated by Django 2.0.6 on 2018-12-29 19:52

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_auto_20181229_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagesblock',
            name='html_after_block',
        ),
        migrations.RemoveField(
            model_name='pagesblock',
            name='html_before_block',
        ),
        migrations.AddField(
            model_name='pagesblock',
            name='html',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Переопределяющий HTML для блока'),
        ),
    ]
