from django.db import models

# Create your models here.
class Podt(models.Model):
    title=models.CharField(max_length=150)
    desc=models.TextField()