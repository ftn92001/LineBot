# Generated by Django 4.1.1 on 2022-10-05 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BotTest', '0002_photo_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_id', models.CharField(max_length=255)),
                ('money', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DailyAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('line_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_attendance', to='BotTest.lineuser')),
            ],
        ),
    ]
