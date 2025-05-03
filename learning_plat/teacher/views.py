from django.shortcuts import render, redirect
import string
import random
from django.contrib import messages
from .models import Course
from lesson.models import Lesson
from accounts.models import Student, User
from assignment.models import Assignment

# Create your views here.
def generate_code():
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(characters, k=6))
    return code

def create_course(request):
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        color = request.POST['color']
        code = generate_code()
        while True:
            if Course.objects.filter(courseId = code).exists():
                code = generate_code()
              
            else:
                break
            

        context = {
            'title' : title,
            'desc' : desc,
            'color' : color
        }

        if len(title) < 0:
            context['title_err'] = 'Поле назви не може бути пустим'
            return render(request, 'teacher/create_course.html', context)
        if len(desc) < 0:
            context['desc_err'] = 'Опис не може бути пустим'
            return render(request, 'teacher/create_course.html', context)
        
        course = Course.objects.create(
            title = title,
            desc = desc,
            color = color,
            courseId = code,
            isArchived = False,
            teacher = request.user
        )
        course.save()

        messages.success(request,'Курс створено!')
        return redirect('/')
    return render(request, 'teacher/create_course.html')

def display_courses(request):
    teacher = request.user
    courses = Course.objects.filter(teacher = teacher)

    context = {
        'courses': courses
    }

    return render(request, 'teacher/display_courses.html', context)

def my_assignments(request):
    teacher = request.user

    courses = Course.objects.filter(teacher=teacher, isArchived__in=[False, None])
    print(courses)

    lessons = Lesson.objects.filter(course__in=courses)
    print(lessons)

    assignments = Assignment.objects.filter(lesson__in=lessons).order_by('-lesson__createdAt')
    print(assignments)

    context = {
        'assignments': assignments,
    }

    return render(request, 'teacher/my_assignments.html', context)