from django.urls import path, include
from student.views import connect_to_course, view_my_courses, leave_course
from course.views import view_course

urlpatterns = [
    path('connect_course/', connect_to_course, name='connect_to_course'),
    path('my_courses/', view_my_courses, name='view_my_courses'),
    path('leave_course/<str:courseId>/', leave_course, name='leave_course'),
    path('my_courses/<str:courseId>/', view_course, name='view_course_student')
]
