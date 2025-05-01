from django.shortcuts import render, redirect
from lesson.models import Lesson
from django.contrib import messages
from .models import Assignment

def create_assignment(request, courseId, lessonId):
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['content']
        due_date = request.POST['due_date']


        context = {
            'title' : title,
            'description' : desc,
            'due_date' : due_date
        }

        if len(title) < 0:
            context['title_err'] = 'Поле назви не може бути пустим'
            return render(request, 'assignment/create_assignment.html', context)
        if len(desc) < 0:
            context['content_err'] = 'Опис не може бути пустим'
            return render(request, 'assignment/create_assignment.html', context)
        
        lesson = Lesson.objects.get(
            id = lessonId
        )
        
        assignment = Assignment.objects.create(
            title = title,
            lesson = lesson,
            desc = desc,
            due_date = due_date,
        )
        assignment.save()

        messages.success(request,'Завдання створено!')
        return redirect(f'/teacher/courses/{courseId}/{lessonId}/')
    return render(request,'assignment/create_assignment.html')

def edit_assignment(request, courseId, lessonId):
    lesson = Lesson.objects.get(id = lessonId)
    assignment = Assignment.objects.get(lesson=lesson)
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        due_date = request.POST['due_date']


        context = {
            'title' : title,
            'desc' : desc,
            'due_date' : due_date
        }

        if len(title) < 0:
            context['title_err'] = 'Поле назви не може бути пустим'
            return render(request, 'assignment/create_assignment.html', context)
        if len(desc) < 0:
            context['content_err'] = 'Опис не може бути пустим'
            return render(request, 'assignment/create_assignment.html', context)
        
        assignment.title = title
        assignment.desc = desc
        assignment.due_date = due_date
        assignment.save()

        messages.success(request,'Завдання змінено!')
        return redirect(f'/teacher/courses/{courseId}/{lessonId}/')
    return render(request,'assignment/edit_assignment.html', {'assignment': assignment})

def delete_assignment(request, courseId, lessonId):
    lesson = Lesson.objects.get(id = lessonId)
    assignment = Assignment.objects.get(lesson = lesson)
    assignment.delete()

    messages.success(request,'Завдання успішно видалено!')
    return redirect(f'/teacher/courses/{courseId}/{lessonId}/')