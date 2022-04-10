from django.db import models
from django.contrib.auth.models import User
import uuid


class Student(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    username = models.CharField(max_length=256)
    student_id = models.CharField(max_length=256, unique=True)
    date_registered = models.DateTimeField(auto_now_add=True)    
    exams = models.ManyToManyField("Exam", through="Student_on_Exam")

    def __str__(self):
        return f"{self.username=}\n\t{self.student_id=}\n\t{self.date_registered=}\n\t{self.exams.count()=}"

class Exam(models.Model):
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
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()

    def __str__(self):
        return f"{self.exam_name=}\n\t{self.course_name=}\n\t{self.course_id=}\n\t{self.num_questions=}\n\t{self.graded=}\n\t{self.total_marks=}" + \
            f"\n\t{self.date_registered=}\n\t{self.open_time=}\n\t{self.close_time=}"

class Student_on_Exam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student_marks = models.DecimalField(max_digits=11, decimal_places=5)
    is_practice = models.BooleanField(default=False, )
    date_student_finished = models.DateTimeField()
    
    def __str__(self):
        return f"{self.student.username=}\n\t{self.exam.exam_name=}\n\t{self.student_marks=}\n\t{self.is_practice=}\n\t{self.date_student_finished=}"