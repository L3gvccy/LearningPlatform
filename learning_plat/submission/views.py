from django.shortcuts import render, redirect
from django.contrib import messages
from teacher.models import Course
from lesson.models import Lesson
from assignment.models import Assignment
from accounts.models import Student
from .models import Submission

def submit(request, courseId, lessonId):
    if request.method == 'POST':
        course = Course.objects.get(courseId=courseId)
        lesson = Lesson.objects.get(id = lessonId)
        assignment = Assignment.objects.get(lesson = lesson)
        student = Student.objects.get(user = request.user)

        file_url = request.POST['file_url']

        if Submission.objects.filter(assignment = assignment, student = student).exists():
            submission = Submission.objects.get(assignment = assignment, student = student)
            submission.grade = 0
            submission.file_url = file_url
            messages.success(request, 'Завдання успішно змінено!')
        else:
            submission = Submission.objects.create(
                file_url = file_url,
                grade = 0,
                student = student,
                assignment = assignment
            )
            messages.success(request, 'Завдання успішно прикріплено!')
        
        submission.save()
        return redirect('view_lesson', courseId=courseId, lessonId=lessonId)
    
def delete_submission(request, courseId, lessonId):
    lesson = Lesson.objects.get(id = lessonId)
    assignment = Assignment.objects.get(lesson = lesson)
    student = Student.objects.get(user = request.user)
    submission = Submission.objects.get(assignment = assignment, student = student)
    submission.delete()

    messages.success(request, 'Прикріплене завдання успішно видалене!')
    return redirect('view_lesson', courseId=courseId, lessonId=lessonId)
