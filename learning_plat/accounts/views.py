from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import User, Student

# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

def logout(request):
    auth.logout(request)
    messages.success(request, "Ви успішно вийшли з акауту")
    return redirect('/')

def register_student(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['pass']
        confirm_password = request.POST['confirm_pass']
        email = request.POST['email']
        last_name = request.POST['lastname']
        first_name = request.POST['firstname']

        context = {
            'login': login or '',
            'email': email,
            'lastname': last_name,
            'firstname': first_name
        }

        if password != confirm_password:
            context['pass_err'] = 'Введені паролі не співпадають'
            return render(request, 'accounts/register.html', context)

        # Спочатку створюємо користувача
        user = User.objects.create_user(
            username=login,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Потім створюємо студента, прив'язуючи до юзера
        student = Student.objects.create(
            user=user,
            courses_id=[]
        )
        student.save()

        messages.success(request, "Реєстрація успішна!")
        return redirect('/')
    
    return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['pass']

        user = auth.authenticate(username=login, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Вітаємо, {user.first_name}! Ви увійшли в систему.")
            return redirect('/')
        else:
            context = {
                'login': login,
                'pass_err': "Невірне ім’я користувача або пароль."
            }
            
            return render(request, 'accounts/login.html', context)

    return render(request, 'accounts/login.html')