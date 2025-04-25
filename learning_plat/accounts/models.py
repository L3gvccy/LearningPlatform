from django.contrib.auth.models import AbstractUser
from djongo import models

class User(AbstractUser):
    pass

class Student(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student'
    )
    courses_id = models.JSONField(default=list)

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='teacher'
    )

    def __str__(self):
        return self.user.username