# Generated by Django 2.1.7 on 2019-05-15 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Software', '0006_auto_20190515_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='6xYM59H3', max_length=10),
        ),
    ]
