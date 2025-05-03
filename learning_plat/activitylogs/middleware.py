from .models import ActivityLogs

class StudentActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and not (request.user.is_staff or request.user.is_superuser):
            ActivityLogs.objects.create(
                student=request.user,
                action=f"Відвідав {request.path}",
                path=request.path
            )

        return response
