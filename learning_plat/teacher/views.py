from django.shortcuts import render, redirect
import string
import random

# Create your views here.
def generate_code():
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(characters, k=6))
    return code

def create_course(request):
    pass