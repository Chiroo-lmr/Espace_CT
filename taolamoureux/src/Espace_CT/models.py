from datetime import datetime
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    images = models.ImageField(upload_to='images/', default='images/missing-file.jpg')
    url_placeholder = models.CharField(max_length=100, default="lien")
    url = models.URLField()
    priority = models.IntegerField(default=0)
    date = models.DateField(default="None", blank=True, null=True)
    
    def __str__(self):
        return self.title

