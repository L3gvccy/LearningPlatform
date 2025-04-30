from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Lesson
from teacher.models import Course


def create_lesson(request, courseId):
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
        
        course = Course.objects.get(
            courseId = courseId
        )

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
    return render(request,'lesson/create_lesson.html')
        

        
    
