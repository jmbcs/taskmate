from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.html import format_html


class Todo(models.Model):
    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
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

    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    description = models.CharField(max_length=300)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="TO_DO")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField()
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=PRIORITY_LOW,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
    )
    notes = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='other'
    )

    def __str__(self):
        return f"{self.description} ({self.get_status_display()})"

    def get_badge_html(self, label, color):
        """Returns HTML for a badge with the specified label and color"""
        return format_html(
            '<span class="badge badge-sm  border-none lg:badge-md  {}">{}</span>',
            color,
            label,
        )

    def get_status(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def get_priority(self):
        return dict(self.PRIORITY_CHOICES)[self.priority]

    def get_category(self):
        return dict(self.CATEGORY_CHOICES)[self.category]

    def get_status_display(self):
        """Returns the current task status or 'Unknown'"""
        try:
            status_label = dict(self.STATUS_CHOICES)[self.status]
            color_map = {
                'TO_DO': 'bg-blue-500',
                'STALLED': 'bg-gray-500',
                'IN_PROGRESS': 'bg-orange-500',
                'COMPLETED': 'bg-green-500',
            }
            return self.get_badge_html(
                status_label, color_map.get(self.status, 'bg-gray-500')
            )
        except KeyError:
            return self.get_badge_html('Unknown', 'bg-gray-500')

    def get_priority_display(self):
        """Returns the current task priority or 'Unknown'"""
        try:
            priority_label = dict(self.PRIORITY_CHOICES)[self.priority]
            color_map = {
                self.PRIORITY_LOW: 'badge-success',
                self.PRIORITY_MEDIUM: 'badge-warning',
                self.PRIORITY_HIGH: 'badge-error',
            }
            return self.get_badge_html(
                priority_label, color_map.get(self.priority, 'badge-error')
            )
        except KeyError:
            return self.get_badge_html('Unknown', 'badge-error')

    def get_category_display(self):
        """Returns the current task category or 'Unknown'"""
        try:
            category_label = dict(self.CATEGORY_CHOICES)[self.category]
            color_map = {
                'work': 'bg-blue-300',
                'personal': 'bg-purple-300',
                'shopping': 'bg-teal-300',
                'health': 'bg-orange-300',
            }
            return self.get_badge_html(
                category_label, color_map.get(self.category, 'bg-gray-300')
            )
        except KeyError:
            return self.get_badge_html('Unknown', 'bg-gray-300')
