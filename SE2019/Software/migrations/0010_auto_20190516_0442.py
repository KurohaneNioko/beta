# Generated by Django 2.1.7 on 2019-05-15 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Software', '0009_auto_20190516_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='d_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='TLkHjIPw', max_length=10),
        ),
    ]
