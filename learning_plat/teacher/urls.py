from django.urls import path, include
from teacher.views import create_course, display_courses, my_assignments
from course.views import view_course, edit_course, remove_student, archive_course, delete_course
from lesson.views import create_lesson
from assignment.views import create_assignment, edit_assignment, delete_assignment
from lesson.views import create_lesson, view_lesson, edit_lesson, delete_lesson
from submission.views import submission_list

urlpatterns = [
    # Курс
    path('create_course/', create_course, name='create_course'),
    path('courses/', display_courses, name='display_courses'),
    path('courses/<str:courseId>/', view_course, name='view_course_teacher'),
    path('courses/edit/<str:courseId>/', edit_course, name='edit_course'),
    path('courses/archive/<str:courseId>/', archive_course, name='archive_course'),
    path('courses/delete/<str:courseId>/', delete_course, name='delete_course'),
    path('courses/<str:courseId>/remove_student/<int:studentId>', remove_student, name='remove_student'),

    # Урок
    path('courses/<str:courseId>/create_lesson/', create_lesson, name='create_lesson'),
    path('courses/<str:courseId>/<str:lessonId>/', view_lesson, name='view_lesson'),
    path('courses/<str:courseId>/<str:lessonId>/edit/', edit_lesson, name='edit_lesson'),
    path('courses/<str:courseId>/<str:lessonId>/delete/', delete_lesson, name='delete_lesson'),

    # Завдання
    path('courses/<str:courseId>/<str:lessonId>/create_assignment/', create_assignment, name='create_assignment'),
    path('courses/<str:courseId>/<str:lessonId>/edit_assignment/', edit_assignment, name='edit_assignment'),
    path('courses/<str:courseId>/<str:lessonId>/delete_assignment/', delete_assignment, name='delete_assignment'),
    path('my_assignments/', my_assignments, name='my_assignments_teacher'),

    
    # Подані роботи (submission)
    path('courses/<str:courseId>/<str:lessonId>/submissions/', submission_list, name='submission_list'),

]