from django.shortcuts import render, redirect
from .forms import RegisterForm


def landing_page(request):
    return render(request, 'landing.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # або головна сторінка
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})