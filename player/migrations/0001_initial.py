# Generated by Django 5.1.2 on 2025-03-26 19:18

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position', models.IntegerField(default=0)),
                ('cash', models.IntegerField(default=1500)),
                ('jail_free_card', models.IntegerField(default=0)),
                ('house', models.IntegerField(default=0)),
                ('hotel', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
