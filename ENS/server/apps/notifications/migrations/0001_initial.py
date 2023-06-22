# Generated by Django 4.2.2 on 2023-06-22 11:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationTemplate',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('send_time', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
