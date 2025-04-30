from djongo import models
from teacher.models import Course

class Lesson(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=512)
    type = models.CharField(max_length=32)
    createdAt = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lesson_course'
    )
    link = models.CharField(max_length=512, null=True, blank=True)