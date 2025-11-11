from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):    
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    STATUS_CHOICES = {
        TO_DO: "to_do",
        IN_PROGRESS: "in_progress",
        REVIEW: "review",
        DONE: "done"
    }

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    PRIORITY_CHOICES = {
        LOW: "low",
        MEDIUM: "medium",
        HIGH: "high"
    }

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=TO_DO)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default=MEDIUM)
    due_date = models.DateField(default=timezone.now)

    