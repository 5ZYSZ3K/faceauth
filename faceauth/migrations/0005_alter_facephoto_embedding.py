# Generated by Django 4.2.7 on 2024-01-14 09:42

from django.db import migrations
import pgvector.django


class Migration(migrations.Migration):
    dependencies = [
        ("faceauth", "0004_alter_facephoto_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facephoto",
            name="embedding",
            field=pgvector.django.VectorField(dimensions=512),
        ),
    ]
