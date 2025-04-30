from django.shortcuts import render, redirect
from django.contrib import messages
from teacher.models import Course
from lesson.models import Lesson
from accounts.models import Student, User

# Create your views here.
def view_course(request, courseId):
    course = Course.objects.get(courseId = courseId)
    lessons = Lesson.objects.filter(course_id = course).order_by('-createdAt')
    students = Student.objects.all().filter(courses_id__contains = courseId)

    context = {
        'course': course,
        'lessons' : lessons,
        'students' : students
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

def remove_student(request, courseId, studentId):
    student = Student.objects.get(id = studentId)
    name = student.user.get_full_name()

    student.courses_id.remove(courseId)
    student.save()

    messages.success(request, f'Студента {name} було вилучено!')
    return redirect(f'/teacher/courses/{courseId}/')

def archive_course(request, courseId):
    course = Course.objects.get(courseId = courseId)
    if course.isArchived:
        course.isArchived = False
        messages.success(request, f'Курс { course.title } було розархівовано.')
    else:
        course.isArchived = True 
        messages.success(request, f'Курс { course.title } було архівовано.') 

    course.save()    

    return redirect(f'/teacher/courses/{courseId}/')