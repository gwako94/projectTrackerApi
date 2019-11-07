from django.db import models

class Project(models.Model):
    """ project model """
    title = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
