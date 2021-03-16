from django.db import models

# Create your models here.
class Graph(models.Model):
    title = models.CharField(max_length=100)
    caption = models.TextField(max_length=1000)
    technology = models.CharField(max_length=20)
    updated = models.DateField(auto_now=False)
    bokeh_html = models.TextField(max_length=100000)
    source = models.CharField(max_length=15)
    source_url = models.URLField()
    download_data_link = models.URLField()
    topic = models.CharField(max_length=20, default="topic")



