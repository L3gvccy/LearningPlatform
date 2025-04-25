from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Teacher

# Кастомний UserAdmin, щоб додавати всі поля до адмін-панелі
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')}
        ),
    )

# Зареєструємо кастомний UserAdmin
admin.site.register(User, CustomUserAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'courses_id')
    search_fields = ('user__username',)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

# Зареєструємо моделі Student та Teacher
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)