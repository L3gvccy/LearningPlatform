from teacher.models import Course
from accounts.models import Student
from django.contrib import messages
from django.shortcuts import redirect, render

def connect_to_course(request):
    if request.method == 'POST':
        course_code = request.POST.get('course_code')

        try:
            course = Course.objects.get(courseId=course_code)
        except Course.DoesNotExist:
            messages.error(request, 'Курс з таким кодом не знайдено.')
            return redirect(request.META.get('HTTP_REFERER', '/'))  

        student = request.user.student
        
        if course.courseId in student.courses_id:
            messages.warning(request, 'Ви вже підключені до цього курсу.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        student.courses_id.append(course.courseId)
        student.save()

        messages.success(request, f'Ви успішно підключились до курсу: {course.title}')
        return redirect(request.META.get('HTTP_REFERER', '/'))

def view_my_courses(request):
    if not request.user.is_authenticated:
        messages.error(request, "Вам потрібно увійти в систему, щоб переглянути курси.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, "Ваш акаунт не має ролі студента.")
        return redirect('/')

    courses = Course.objects.filter(courseId__in=student.courses_id)

    context = {
        'courses': courses,
    }
    return render(request, 'student/my_courses.html', context)

def leave_course(request, courseId):
    if not request.user.is_authenticated:
        messages.error(request, "Вам потрібно увійти в систему, щоб вийти з курсу.")
        return redirect('login')

    student = Student.objects.get(user=request.user) 
    course = Course.objects.get(courseId=courseId)  

    if courseId in student.courses_id:
        student.courses_id.remove(courseId)
        student.save()
        messages.success(request, f"Ви успішно вийшли з курсу {course.title}.")
    else:
        messages.error(request, "Цей курс не знайдений у вашому списку.")

    return redirect(request.META.get('HTTP_REFERER', '/'))