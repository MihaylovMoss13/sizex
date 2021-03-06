# Generated by Django 2.0.6 on 2018-07-12 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20180712_1931'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.AlterField(
            model_name='feedback',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='email',
            field=models.CharField(blank=True, max_length=255, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='Телефон'),
        ),
    ]
