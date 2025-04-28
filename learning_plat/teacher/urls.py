from django.urls import path, include
from teacher.views import create_course

urlpatterns = [
    path('create_course/', create_course, name='create_course')
]