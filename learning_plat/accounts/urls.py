from django.urls import path, include
from accounts.views import logout, register_student, login

urlpatterns = [
    path('register/', register_student, name='register_student'), 
    path('login/', login, name='login'), 
    path('logout/', logout, name="logout")
]