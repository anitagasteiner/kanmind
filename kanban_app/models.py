from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, related_name='member_of_boards')
    
    def __str__(self):
        return self.title
    

class Ticket(models.Model):
    title = models.CharField(max_length=50)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tickets')


class Task(models.Model):    
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    STATUS_CHOICES = [
        (TO_DO, "To Do"),
        (IN_PROGRESS, "In Progress"),
        (REVIEW, "Review"),
        (DONE, "Done")
    ]

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    PRIORITY_CHOICES = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High")
    ]

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=TO_DO)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=MEDIUM)
    due_date = models.DateField(default=timezone.now)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title


