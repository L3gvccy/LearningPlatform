from django.shortcuts import render, redirect
from lesson.models import Lesson
from django.contrib import messages
from .models import Assignment
from teacher.models import Course

def create_assignment(request, courseId, lessonId):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['content']
        due_date = request.POST['due_date']


        context = {
            'title' : title,
            'description' : description,
            'due_date' : due_date
        }

        if len(title) < 0:
            context['title_err'] = 'Поле назви не може бути пустим'
            return render(request, 'assignment/create_assignment.html', context)
        if len(description) < 0:
            context['content_err'] = 'Опис не може бути пустим'
            return render(request, 'assignment/create_assignment.html', context)
        
        lesson = Lesson.objects.get(
            lessonId = lessonId
        )

        course = Course.objects.get(
            courseId = courseId
        )
        
        assignment = Assignment.objects.create(
            title = title,
            lesson = lesson,
            description = description,
            due_date = due_date,
        )
        assignment.save()

        messages.success(request,'Завдання створено!')
        return redirect(f'/')
    return render(request,'assignment/create_assignment.html')

