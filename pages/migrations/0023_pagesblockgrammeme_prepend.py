# Generated by Django 2.0.6 on 2019-08-12 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0022_auto_20190812_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagesblockgrammeme',
            name='prepend',
            field=models.BooleanField(default=False, verbose_name='Prepend?'),
        ),
    ]
