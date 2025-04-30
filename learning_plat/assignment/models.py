from django.db import models
from lesson.models import Lesson

class Assignment(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=512)
    due_date = models.DateTimeField()
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='assignment_lesson'
    )
