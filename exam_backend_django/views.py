import json
from functools import wraps

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User

from . import models

# Decorators

def require_params(*register_params):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            data = json.loads(request.body)
            if not any(param in data for param in register_params):
                return JsonResponse({"status":"failed", "message": "wrong parameters, or wrong format."}, status=400)
            return function(request, *args, **kwargs)
        return wrapper
    return decorator

def login_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"message": "user not authenticated."}, status=401)
        return function(request, *args, **kwargs)
    return wrapper

def exception_catcher(function):
    def wrapper(request, *args, **kwargs):
        try:
            return function(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({"status":"failed", "message": f"database exception {e.message}."}, status=400)
    return wrapper

# Views

@csrf_exempt
@require_http_methods(["POST"])
@require_params("student_id", "password", "nickname")
def register_view(request):
    data = json.loads(request.body)
    user = User.objects.create_user(username=data["student_id"], password=data["password"])
    models.Student.objects.create(student_id=data["student_id"], nickname=data["nickname"], user=user)
    return JsonResponse({"message": "success"}, status=200)
    
@csrf_exempt
@require_http_methods(["POST"])
@require_params("student_id", "password")
def login_view(request):
    data = json.loads(request.body)
    user = authenticate(request, username=data["student_id"], password=data["password"])
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "success"}, status=200)
    else:
        return JsonResponse({"status":"failed", "message": "Incorrect login details"}, status=401)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "success"}, status=200)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
@require_params("start_index", "end_index")
def get_exams_view(request):
    MAX_EXAMS_PER_REQUEST = 100
    data = json.loads(request.body)
    if MAX_EXAMS_PER_REQUEST < data["end_index"] - data["start_index"]:
        return JsonResponse({"status":"failed", "message": "wrong parameters, or wrong format."}, status=400)
    fields = [
        "exam_name",
        "course_name",
        "course_id",
        "description",
        "date_registered",
        "open_time",
        "close_time",
    ]
    exams = models.Exam.objects.order_by("-date_registered")[data["start_index"]:data["end_index"]].values(*fields)
    return JsonResponse({"exams": list(exams), "message": "success"}, status=200)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
@require_params("exam_name", "start_index", "end_index")
def get_ranking_view(request):
    MAX_EXAMS_PER_REQUEST = 100
    data = json.loads(request.body)
    exam = models.Exam.objects.get(exam_name=data["exam_name"])
    if MAX_EXAMS_PER_REQUEST < data["end_index"] - data["start_index"]:
        return JsonResponse({"status":"failed", "message": "wrong parameters, or wrong format."}, status=400)
    ranking = models.Student_on_Exam.objects.filter(
        exam=exam
        ).order_by("-student_marks") \
        .select_related("student")[data["start_index"]:data["end_index"]]
    ranking = [
        {"nickname": attempt.student.nickname, "marks": attempt.student_marks} for attempt in ranking
    ]
    return JsonResponse({"ranking": ranking, "message": "success"}, status=200)

# @csrf_exempt
#
# @login_required
# @require_http_methods(["POST"])
# @require_params("exam_name")
# def get_past_exams_view(request):
#     MAX_EXAMS_PER_REQUEST = 100
#     data = json.loads(request.body)
#     if MAX_EXAMS_PER_REQUEST < data["end_index"] - data["start_index"]:
#         return JsonResponse({"status":"failed", "message": "wrong parameters, or wrong format."}, status=400)
#     exam = models.Exam.objects.get(exam_name=data["exam"])
#     ranking = models.Student_on_Exam.objects.filter(
#         exam=exam
#         ).select_related("student") 
#     ranking = [
#         {"nickname": attempt.student.nickname, "marks": attempt.student_marks} for attempt in ranking
#     ]
#     return JsonResponse({"ranking": ranking, "message": "success"}, status=200)
