from django.urls import path, include
from teacher.views import create_course, display_courses

urlpatterns = [
    path('create_course/', create_course, name='create_course'),
    path('courses/', display_courses, name='display_courses')
]