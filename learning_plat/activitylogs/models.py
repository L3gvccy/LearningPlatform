from django.db import models
from accounts.models import User

class ActivityLogs(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

