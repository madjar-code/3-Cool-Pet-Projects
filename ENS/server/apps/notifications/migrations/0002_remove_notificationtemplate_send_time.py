# Generated by Django 4.2.2 on 2023-07-11 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationtemplate',
            name='send_time',
        ),
    ]
