from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)

class Messages(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

class Event(models.Model):
    title = models.CharField(max_length=200)  # e.g., "Football Match"
    place = models.CharField(max_length=200)  # e.g., "Stadium Name"
    event_time = models.DateTimeField()  # Store event time
    description = models.TextField()  # Optional description about the event

    def __str__(self):
        return f'{self.title} - {self.place}'

from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)

class Messages(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

class Event(models.Model):
    title = models.CharField(max_length=200)  # e.g., "Football Match"
    place = models.CharField(max_length=200)  # e.g., "Stadium Name"
    event_time = models.DateTimeField()  # Store event time
    description = models.TextField()  # Optional description about the event

    def __str__(self):
        return f'{self.title} - {self.place}'

# main_app/models.py
from django.db import models

class ComplaintRating(models.Model):
    complaint = models.ForeignKey('Complaint', on_delete=models.CASCADE)  # הקשר לתלונה
    rating = models.IntegerField()  # הדירוג (1-5)
    created_at = models.DateTimeField(auto_now_add=True)  # זמן יצירת הדירוג

    def __str__(self):
        return f"Rating for Complaint {self.complaint.id}: {self.rating}"
# main_app/models.py

from django.db import models

class Complaint(models.Model):
    description = models.TextField()
    status = models.CharField(max_length=20)
    # שדות נוספים שאתה רוצה לשמור בתלונה

    def __str__(self):
        return self.description
