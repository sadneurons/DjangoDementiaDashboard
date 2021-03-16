from django.db import models

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=10000)
    date = models.DateField()
    topic = models.CharField(max_length=20)
