"""
Models for the Kanmind backend Kanban application.

This module defines:
- Board: A Kanban board with an owner and member users.
- Task: Work items tracked on a board, including status, priority, and assignment.
- Comment: User-authored comments attached to tasks.
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date


class Board(models.Model):
    """
    Represents a Kanban board.

    Fields:
        title (str): Board title.
        owner (User): The user who created and owns the board.
        members (QuerySet[User]): Users who have access to the board.
    """
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_boards'
    )
    members = models.ManyToManyField(
        User,
        related_name='member_of_boards'
    )
    
    def __str__(self):
        """Return the board title as its string representation."""
        return self.title
    

class Task(models.Model):
    """
    Represents a task within a Kanban board.

    Fields:
        title (str): Task title.
        description (str): Detailed task description.
        assignee (User|None): User responsible for executing the task.
        reviewer (User|None): User responsible for reviewing the task.
        status (str): Workflow status from predefined choices.
        priority (str): Task urgency level.
        due_date (date): Deadline for the task.
        board (Board): Board to which the task belongs.

    Status values:
        to_do, in_progress, review, done

    Priority values:
        low, medium, high
    """
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
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_tasks'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviewed_tasks'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=TO_DO
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default=MEDIUM
    )
    due_date = models.DateField(default=date.today)
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    def __str__(self):
        """Return the task title as its string representation."""
        return self.title


class Comment(models.Model):
    """
    Represents a comment attached to a task.

    Fields:
        created_at (datetime): Timestamp of comment creation.
        author (User): User who authored the comment.
        content (str): Text content of the comment.
        task (Task): Associated task.
    """
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='own_comments'
    )
    content = models.TextField(max_length=500)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        """Return the comment content as its string representation."""
        return self.content
    
