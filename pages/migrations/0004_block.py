# Generated by Django 2.0.6 on 2018-07-14 20:19

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20180712_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Название блока')),
                ('html', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Html блока')),
                ('where', models.IntegerField(choices=[(0, 'Сверху'), (1, 'Снизу')], default=0, verbose_name='Расположение')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Очередность')),
                ('page', models.ManyToManyField(blank=True, null=True, to='pages.Pages', verbose_name='Страница')),
            ],
            options={
                'verbose_name': 'Html блок',
                'verbose_name_plural': 'Html блоки',
                'ordering': ('order',),
            },
        ),
    ]