# Generated by Django 2.0.6 on 2018-07-14 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='page',
            field=models.ManyToManyField(blank=True, to='pages.Pages', verbose_name='Страница'),
        ),
    ]