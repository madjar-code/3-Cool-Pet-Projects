# Generated by Django 4.2.2 on 2023-07-03 07:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
        ('reports', '0002_alter_notificationstate_contact_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationstate',
            name='notification_template',
        ),
        migrations.CreateModel(
            name='NotificationSession',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('notification_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='notifications.notificationtemplate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='notificationstate',
            name='noticication_session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='states', to='reports.notificationsession'),
        ),
    ]