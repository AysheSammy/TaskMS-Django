from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("list", kwargs={"pk": self.pk})

class Task(models.Model):
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, null=True, blank=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    PRIORITY_CHOICES = [
        ('I', 'Important'),
        ('NI', 'Not Important'),
        ('VI', 'Very Important'),
    ]
    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default='NI',
    )
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']