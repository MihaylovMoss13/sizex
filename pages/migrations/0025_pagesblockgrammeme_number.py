# Generated by Django 2.0.6 on 2019-08-12 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0024_auto_20190812_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagesblockgrammeme',
            name='number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Номер граммемы'),
        ),
    ]
