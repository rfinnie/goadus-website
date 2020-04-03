# Generated by Django 3.0.5 on 2020-04-03 01:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import goadus.models
import goadus.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(default=goadus.utils.werder_name, unique=True)),
                ('original_filename', models.CharField(max_length=200)),
                ('content_type', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageSet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(default=goadus.utils.werder_name, unique=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_expires', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.ImageField(max_length=200, storage=goadus.models.IGoadStorage(), upload_to='')),
                ('type', models.CharField(choices=[('uploaded', 'Unsanitized original image'), ('original', 'Original image'), ('medium', 'Resized image'), ('thumbnail', 'Thumbnail image')], max_length=200)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goadus.Image')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='image_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goadus.ImageSet'),
        ),
    ]
