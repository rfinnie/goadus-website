# Generated by Django 3.0.5 on 2020-04-23 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import goadus.utils
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("goadus", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApiKey",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "slug",
                    models.SlugField(default=goadus.utils.werder_api_key, unique=True),
                ),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                ("date_expires", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        )
    ]
