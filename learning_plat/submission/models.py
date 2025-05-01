from django.db import models
from assignment.models import Assignment
from student.models import Student

class Submission(models.Model):
    file_url = models.URLField()
    grade = models.IntegerField(default=0)
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submission_assignment'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='submission_student'
    )
    
    