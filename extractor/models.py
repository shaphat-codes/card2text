from django.db import models

# Create your models here.

class Card(models.Model):
    url = models.CharField(max_length=10000)
