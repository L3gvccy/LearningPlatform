from django.urls import path, include
from teacher.views import create_course, display_courses
from course.views import view_course, edit_course, remove_student, archive_course
from lesson.views import create_lesson
from assignment.views import create_assignment
from lesson.views import create_lesson, view_lesson

urlpatterns = [
    path('create_course/', create_course, name='create_course'),
    path('courses/', display_courses, name='display_courses'),
    path('courses/<str:courseId>/', view_course, name='view_course_teacher'),
    path('courses/edit/<str:courseId>/', edit_course, name='edit_course'),
    path('courses/archive/<str:courseId>/', archive_course, name='archive_course'),
    path('courses/<str:courseId>/create_lesson/', create_lesson, name='create_lesson'),
    path('courses/<str:courseId>/remove_student/<int:studentId>', remove_student, name='remove_student'),
    path('courses/<str:courseId>/<str:lessonId>/create_assignment/', create_assignment, name='create_assignment'),
    path('courses/<str:courseId>/<str:lessonId>/', view_lesson, name='view_lesson'),
]