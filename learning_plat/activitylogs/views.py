from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from accounts.models import User
from .models import ActivityLogs

@login_required
def student_activity(request, student_id):
    student = get_object_or_404(User, id=student_id)
    activities = ActivityLogs.objects.filter(student=student)
    return render(request, 'teacher/student_activity.html', {
        'student': student,
        'activities': activities
    })