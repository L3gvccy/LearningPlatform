from django.urls import path, include
from teacher.views import create_course, display_courses, view_course

urlpatterns = [
    path('create_course/', create_course, name='create_course'),
    path('courses/', display_courses, name='display_courses'),
    path('course/<str:courseId>/', view_course, name='view_course_teacher')
]