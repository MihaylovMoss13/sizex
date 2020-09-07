# Generated by Django 2.0.6 on 2018-10-01 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_pages_ymap'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Название региона'),
        ),
        migrations.AddField(
            model_name='domain',
            name='scripts',
            field=models.TextField(blank=True, null=True, verbose_name='Доп. скрипты'),
        ),
    ]