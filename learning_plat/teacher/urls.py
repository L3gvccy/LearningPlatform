from django.urls import path, include
from teacher.views import create_course, display_courses
from course.views import view_course, edit_course

urlpatterns = [
    path('create_course/', create_course, name='create_course'),
    path('courses/', display_courses, name='display_courses'),
    path('courses/<str:courseId>/', view_course, name='view_course_teacher'),
    path('courses/edit/<str:courseId>/', edit_course, name='edit_course')
]