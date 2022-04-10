import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from . import models

# login_required

@csrf_exempt
def register_view(request):
    register_params = ("student_id", "password", "username")
    data = json.loads(request.body)
    if request.method != 'POST':
        return JsonResponse({'status':'failed', "message": "The request header isn't a POST request."})
    if not any(param in data for param in register_params):
        return JsonResponse({'status':'failed', "message": "wrong parameters, or wrong format."})
    user = User.objects.create_user(username=data['student_id'], password=data['password'])
    models.Student.objects.create(student_id=data['student_id'], username=data['username'], user=user)
    return JsonResponse({'status':'success'})
    

@csrf_exempt
def login_view(request):
    data = json.loads(request.body)
    if request.method != 'POST':
        return JsonResponse({'status':'failed', "message": "The request header isn't a POST request."})
    if "student_id" not in data or "password" not in data:
        return JsonResponse({'status':'failed', "message": "wrong parameters, or wrong format."})
    user = authenticate(request, username=data['student_id'], password=data['password'])
    if user is not None:
        login(request, user)
        student = User.objects.get(username=user.get_username())
        print(f"{student=}\n\n{dir(student)=}")
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'failed', "message": "Incorrect login details"})

@login_required
def logout_view(request):
    logout(request)
