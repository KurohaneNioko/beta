# Generated by Django 2.1.7 on 2019-04-28 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Software', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='del_user',
            options={'ordering': ['del_time']},
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='Na89FJAC', max_length=10),
        ),
    ]
