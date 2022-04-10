import json
from functools import wraps

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from django.contrib.auth.models import User

from . import models

def require_params(*register_params):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            data = json.loads(request.body)
            if not any(param in data for param in register_params):
                return JsonResponse({'status':'failed', "message": "wrong parameters, or wrong format."})
            return function(request, *args, **kwargs)
        return wrapper
    return decorator

@csrf_exempt
@require_http_methods(["POST"])
@require_params("student_id", "password", "username")
def register_view(request):
    data = json.loads(request.body)
    user = User.objects.create_user(username=data['student_id'], password=data['password'])
    models.Student.objects.create(student_id=data['student_id'], username=data['username'], user=user)
    return JsonResponse({'status':'success'})
    
@csrf_exempt
@require_http_methods(["POST"])
@require_params("student_id", "password")
def login_view(request):
    data = json.loads(request.body)
    user = authenticate(request, username=data['student_id'], password=data['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'failed', "message": "Incorrect login details"})

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({'status':'success'})
