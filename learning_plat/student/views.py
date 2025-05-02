from teacher.models import Course
from accounts.models import Student
from django.contrib import messages
from django.shortcuts import redirect, render
from djongo.database import DatabaseError
from lesson.models import Lesson
from assignment.models import Assignment
from submission.models import Submission
from django.utils import timezone

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

    courses = Course.objects.filter(courseId__in=student.courses_id, isArchived__in=[False, None])

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

def my_assignments(request):
    
    student = Student.objects.get(user=request.user)
    now = timezone.now()

    courses = Course.objects.filter(courseId__in=student.courses_id, isArchived__in=[False, None])
    print(courses)

    lessons = Lesson.objects.filter(course__in=courses)
    print(lessons)

    assignments = Assignment.objects.filter(lesson__in=lessons)
    print(assignments)

    submissions = Submission.objects.filter(student=student)
    submitted_ids = set(submissions.values_list('assignment_id', flat=True))

    completed = []
    pending = []
    missed = []

    for assignment in assignments:
        if assignment.id in submitted_ids:
            completed.append(assignment)
        elif assignment.due_date < now:
            missed.append(assignment)
        else:
            pending.append(assignment)

    pending = sorted(pending, key=lambda a: a.due_date)
    missed = sorted(missed, key=lambda a: a.due_date)

    context = {
        'completed': completed,
        'pending': pending,
        'missed': missed
    }

    return render(request, 'student/my_assignments.html', context)