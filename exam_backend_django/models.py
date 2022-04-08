from email.policy import default
from tabnanny import verbose
from django.db import models
import uuid


class Users(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username = models.CharField(max_length=256)
    student_id = models.CharField(max_length=256, unique=True)
    hashed_password = models.CharField(max_length=1024)
    salt = models.CharField(max_length=1024)
    date_registered = models.DateTimeField(auto_now_add=True)


class Exams(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    exam_name = models.CharField(max_length=256)
    course_name = models.CharField(max_length=256)
    course_id = models.CharField(max_length=256)
    
    exam_content = models.TextField()
    num_questions = models.PositiveIntegerField(blank=True, null=True)
    
    graded = models.BooleanField(default=True)
    total_marks = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    
    date_registered = models.DateTimeField(auto_now_add=True)
    open_time = models.DateTimeField(verbose="Time when the exam can start to be taken")
    close_time = models.DateTimeField(verbose="Time when the exam stops being able to be to be taken")

class User_on_Exam(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exams, on_delete=models.SET_NULL)
    user_marks = models.DecimalField(max_digits=10, decimal_places=5)
    is_practice = models.BooleanField(default=False, verbose=)
    date_user_finished = models.DateTimeField()