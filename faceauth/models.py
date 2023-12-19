from django.contrib.auth.models import User
from django.db import models
from pgvector.django import VectorField


class FacePhoto(models.Model):
    image = models.ImageField(upload_to="static/")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    embedding = VectorField(dimensions=1)
