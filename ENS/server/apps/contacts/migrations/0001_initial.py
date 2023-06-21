# Generated by Django 4.2.2 on 2023-06-21 07:28

from django.db import migrations, models
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=30, null=True, region=None)),
                ('priority_group', models.CharField(choices=[('Low', 'Low Priority'), ('High', 'High Priority'), ('Blacklist', 'Blacklist')], default='Low', max_length=15)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
