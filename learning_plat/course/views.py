from django.shortcuts import render, redirect
from django.contrib import messages
from teacher.models import Course
from lesson.models import Lesson
from accounts.models import Student, User
from assignment.models import Assignment
from submission.models import Submission

# Create your views here.
def view_course(request, courseId):
    course = Course.objects.get(courseId = courseId)
    lessons = Lesson.objects.filter(course_id = course).order_by('-createdAt')
    students = Student.objects.all().filter(courses_id__contains = courseId)
    assignments = Assignment.objects.filter(lesson__course = course).order_by('-lesson__createdAt')
    submissions = None
    submitted_ids = None
    try:
        student = Student.objects.get(user = request.user)
        submissions = Submission.objects.filter(student=student)
        submitted_ids = set(submissions.values_list('assignment_id', flat=True))
    except:
        pass

    context = {
        'course': course,
        'lessons' : lessons,
        'students' : students,
        'assignments': assignments,
        'submitted_ids': submitted_ids
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

def delete_course(request, courseId):
    course = Course.objects.get(courseId = courseId)
    course.delete()
    
    messages.success(request, f'Курс { course.title } було видалено.')
    return redirect('/teacher/courses/')