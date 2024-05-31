from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class User(AbstractUser): ...


class Todo(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    STATUS_CHOICES = [
        ('TO_DO', 'To Do'),
        ('STALLED', 'Stalled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    CATEGORY_CHOICES = [
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('shopping', 'Shopping'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]

    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_description = models.CharField(max_length=300)
    task_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="TO_DO"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
    )
    notes = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='other'
    )

    def __str__(self) -> str:
        return f"{self.task_description} ({self.get_task_status_display()})"

    def get_task_status_display(self) -> str:
        """Returns the curent task status or "Unknown" """
        return dict(self.STATUS_CHOICES).get(self.task_status, 'Unknown')
