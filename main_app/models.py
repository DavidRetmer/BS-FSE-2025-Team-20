from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)