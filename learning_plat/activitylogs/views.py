from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from accounts.models import Student
from teacher.models import Course
from .models import ActivityLogs

def log_activity(student, course, action):
    ActivityLogs.objects.create(
        student = student,
        course = course,
        action = action
    )

@login_required
def student_activity(request, student_id, courseId):
    course = Course.objects.get(courseId = courseId)
    student = Student.objects.get(user_id = student_id)
    activities = ActivityLogs.objects.filter(student=student, course=course)
    return render(request, 'teacher/student_activity.html', {
        'student': student,
        'course': course,
        'activities': activities
    })