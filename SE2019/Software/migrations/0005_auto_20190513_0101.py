# Generated by Django 2.1.7 on 2019-05-12 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Software', '0004_auto_20190512_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introduction',
            field=models.CharField(default='尚待补充', max_length=100, verbose_name='简介'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='ryD40dGS', max_length=10),
        ),
    ]
