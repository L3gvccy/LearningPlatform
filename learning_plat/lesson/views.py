from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Lesson
from teacher.models import Course
from assignment.models import Assignment
from submission.models import Submission
from accounts.models import Student
from activitylogs.views import log_activity


def create_lesson(request, courseId):
    course = Course.objects.get(
        courseId = courseId
    )
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        type = request.POST['type']
        link = request.POST['link']

        context = {
            'title' : title,
            'content' : content,
            'type' : type,
            'link' : link
        }

        if len(title) < 0:
            context['title_err'] = 'Поле назви не може бути пустим'
            return render(request, 'lesson/create_lesson.html', context)
        if len(content) < 0:
            context['content_err'] = 'Опис не може бути пустим'
            return render(request, 'lesson/create_lesson.html', context)

        lesson = Lesson.objects.create(
            title = title,
            content = content,
            type = type,
            link = link,
            course = course
        )
        lesson.save()

        messages.success(request,'Урок створено!')
        return redirect(f'/teacher/courses/{courseId}/')
    
    return render(request,'lesson/create_lesson.html', {'course': course})

def view_lesson(request, courseId, lessonId):
    course = Course.objects.get(courseId = courseId)
    lesson = Lesson.objects.get(id = lessonId)
    assignment = None
    try:
        assignment = Assignment.objects.get(lesson = lesson)
    except:
        pass

    submission = None
    try:
        student = Student.objects.get(user = request.user)
        submission = Submission.objects.get(assignment = assignment, student = student)
    except:
        pass

    context = {
        'course': course,
        'lesson': lesson,
        'assignment': assignment,
        'submission': submission
    }

    if Student.objects.filter(user = request.user).exists():
        student = Student.objects.get(user = request.user)
        log_activity(student, course, f'Переглядав урок {lesson.title}')

    return render(request, 'lesson/view_lesson.html', context)

def edit_lesson(request, courseId, lessonId):
    lesson = Lesson.objects.get(id = lessonId)
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        type = request.POST['type']
        link = request.POST['link']

        context = {
            'title' : title,
            'content' : content,
            'type' : type,
            'link' : link
        }

        if len(title) < 0:
            context['title_err'] = 'Поле назви не може бути пустим'
            return render(request, 'lesson/edit_lesson.html', context)
        if len(content) < 0:
            context['content_err'] = 'Опис не може бути пустим'
            return render(request, 'lesson/edit_lesson.html', context)
        
        lesson.title = title
        lesson.content = content
        lesson.type = type
        lesson.link = link
        lesson.save()

        messages.success(request,'Урок успішно змінено!')
        return redirect('view_lesson', courseId=courseId, lessonId=lessonId)
    
    return render(request, 'lesson/edit_lesson.html', {'lesson': lesson})

def delete_lesson(request, courseId, lessonId):
    lesson = Lesson.objects.get(id = lessonId)
    lesson.delete()

    messages.success(request,'Урок успішно видалено!')
    return redirect('view_course_teacher', courseId=courseId)
