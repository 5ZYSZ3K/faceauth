# Generated by Django 4.2.7 on 2023-12-19 07:37

from django.db import migrations
import pgvector.django


class Migration(migrations.Migration):

    dependencies = [
        ('faceauth', '0002_auto_20231219_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='facephoto',
            name='embedding',
            field=pgvector.django.VectorField(default=[0], dimensions=1),
            preserve_default=False,
        ),
    ]
