from django.shortcuts import render

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Разрешить доступ к админке или авторизованным — по желанию
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        return render(request, 'maintenance.html', status=503)
