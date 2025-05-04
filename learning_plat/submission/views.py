from django.shortcuts import render, redirect
from django.contrib import messages
from teacher.models import Course
from lesson.models import Lesson
from assignment.models import Assignment
from accounts.models import Student
from .models import Submission
from activitylogs.views import log_activity

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

            log_activity(student, course, f'Змінив завдання до уроку {lesson.title}')

        else:
            submission = Submission.objects.create(
                file_url = file_url,
                grade = 0,
                student = student,
                assignment = assignment
            )
            messages.success(request, 'Завдання успішно прикріплено!')

            log_activity(student, course, f'Прикріпив завдання до уроку {lesson.title}')
        
        submission.save()
        return redirect('view_lesson', courseId=courseId, lessonId=lessonId)
    
def delete_submission(request, courseId, lessonId):
    course = Course.objects.get(courseId = courseId)
    lesson = Lesson.objects.get(id = lessonId)
    assignment = Assignment.objects.get(lesson = lesson)
    student = Student.objects.get(user = request.user)
    submission = Submission.objects.get(assignment = assignment, student = student)
    submission.delete()

    messages.success(request, 'Прикріплене завдання успішно видалене!')

    log_activity(student, course, f'Видалив прикріплене завдання до уроку {lesson.title}')

    return redirect('view_lesson', courseId=courseId, lessonId=lessonId)

def submission_list(request, courseId, lessonId):
    course = Course.objects.get(courseId=courseId)
    title = Lesson.objects.get(id=lessonId).title
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        grade = request.POST.get('grade')
        if submission_id and grade is not None:
            try:
                submission = Submission.objects.get(id=submission_id)
                submission.grade = int(grade)
                submission.save()
            except Submission.DoesNotExist:
                pass 

        messages.success(request, 'Оцінка посталенна успішно!')
        return redirect('submission_list', courseId=courseId, lessonId=lessonId)

    lesson = Lesson.objects.get(id=lessonId)
    assignment = Assignment.objects.get(lesson = lesson)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'submission/submission_list.html', {'submissions': submissions, 'course': course, 'title': title, 'lesson': lesson})