from django.urls import path, include
from accounts.views import logout, register_student, login, register_teacher

urlpatterns = [
    path('register/', register_student, name='register_student'),
    path('register-teacher/', register_teacher, name='register_teacher'),
    path('login/', login, name='login'), 
    path('logout/', logout, name="logout")
]