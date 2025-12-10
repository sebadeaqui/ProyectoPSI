from django.db import models

# Create your models here.

class Practica(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.username
