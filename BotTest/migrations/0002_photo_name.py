# Generated by Django 4.1.1 on 2022-09-26 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BotTest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
