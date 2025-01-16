from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)

# haci se crea tablas de sql  .
class Messeges(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
