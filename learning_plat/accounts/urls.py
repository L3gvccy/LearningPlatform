from django.urls import path, include
from accounts.views import landing_page,register

urlpatterns = [
    path('', landing_page, name='landing_page'), 
    path('register/', register, name='register'),
]