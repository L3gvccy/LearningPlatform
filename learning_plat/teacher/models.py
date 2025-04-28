from djongo import models
from accounts.models import User

# Create your models here.

class Course(models.Model):
    courseId = models.CharField(max_length=6,primary_key=True)
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=256)
    teacher = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher'
    )
    color = models.CharField(max_length=7)
    isArchived = models.BooleanField()

