from django.shortcuts import render, redirect
from django.contrib import messages
from teacher.models import Course
from lesson.models import Lesson

# Create your views here.
def view_course(request, courseId):
    course = Course.objects.get(courseId = courseId)
    lessons = Lesson.objects.filter(course_id = course).order_by('-createdAt')

    context = {
        'course': course,
        'lessons' : lessons
    }

    return render(request, 'course/view_course.html', context)

def edit_course(request, courseId):
    course = Course.objects.get(courseId=courseId)
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        color = request.POST['color']

        context = {
            'title' : title,
            'desc' : desc,
            'color' : color
        }

        if len(title) < 0:
            context['title_err'] = 'Поле назви не може бути пустим'
            return render(request, 'teacher/edit_course.html', context)
        if len(desc) < 0:
            context['desc_err'] = 'Опис не може бути пустим'
            return render(request, 'teacher/edit_course.html', context)
        
        course.title = title
        course.desc = desc
        course.color = color
        course.save()

        messages.success(request, 'Зміни було успішно внесено!')
        return redirect(f'/teacher/courses/{courseId}/')
    
    return render(request, 'course/edit_course.html', {'course': course})