from django.urls import path, include
from accounts.views import landing_page

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('register/', landing_page, name='landing_page'), 
]