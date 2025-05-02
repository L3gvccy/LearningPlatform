from django.urls import path, include
from student.views import connect_to_course, view_my_courses, leave_course, my_assignments
from course.views import view_course
from submission.views import submit, delete_submission

urlpatterns = [
    path('connect_course/', connect_to_course, name='connect_to_course'),
    path('my_courses/', view_my_courses, name='view_my_courses'),
    path('leave_course/<str:courseId>/', leave_course, name='leave_course'),
    path('my_courses/<str:courseId>/', view_course, name='view_course_student'),
    path('courses/<str:courseId>/<str:lessonId>/submit/', submit, name='submit'),
    path('courses/<str:courseId>/<str:lessonId>/delete_submission/', delete_submission, name='delete_submission'),
    path('my_assignments/', my_assignments, name='my_assignments')
]
