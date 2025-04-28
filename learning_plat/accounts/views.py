from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import User, Student, Teacher
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

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
            'login': login,
            'email': email,
            'lastname': last_name,
            'firstname': first_name
        }

        if password != confirm_password:
            context['pass_err'] = 'Введені паролі не співпадають'
            return render(request, 'accounts/register.html', context)
        
        if password.length < 3:
            context['pass_err'] = 'Пароль має складатись мінімум з 3 символів'
            return render(request, 'accounts/register.html', context)
        
        if User.objects.filter(username = login).exists():
            context['login_err'] = 'Користувач з таким логіном вже існує'
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

def register_teacher(request):
    if not request.user.is_superuser:
        messages.error(request, "Доступ заборонено: тільки для адміністратора.")
        return redirect('/')

    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['pass']
        confirm_password = request.POST['confirm_pass']
        email = request.POST['email']
        last_name = request.POST['lastname']
        first_name = request.POST['firstname']

        context = {
            'login': login,
            'email': email,
            'lastname': last_name,
            'firstname': first_name
        }

        if password != confirm_password:
            context['pass_err'] = 'Введені паролі не співпадають'
            return render(request, 'accounts/register_teacher.html', context)
        
        if password.length < 3:
            context['pass_err'] = 'Пароль має складатись мінімум з 3 символів'
            return render(request, 'accounts/register.html', context)
        
        if User.objects.filter(username = login).exists():
            context['login_err'] = 'Користувач з таким логіном вже існує'
            return render(request, 'accounts/register.html', context)

        user = User.objects.create_user(
            username=login,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        teacher = Teacher.objects.create(
            user=user
        )
        teacher.save()

        messages.success(request, "Викладача успішно додано!")
        return redirect('/')
    
    return render(request, 'accounts/register_teacher.html')

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

@login_required
def profile_user(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        messages.success(request, "Інформацію оновлено успішно!")
        return redirect('/account/profile/')

    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Старий пароль введено невірно.")
        elif new_password != confirm_password:
            messages.error(request, "Нові паролі не співпадають.")
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Зберегти сесію
            messages.success(request, "Пароль успішно змінено.")
            return redirect('/account/profile/')

    return render(request, 'accounts/change_password.html')