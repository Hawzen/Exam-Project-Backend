import uuid
import json

from random import randint
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from . import utilities

class Student(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    student_id = models.CharField(max_length=256, unique=True)
    nickname = models.CharField(max_length=256)
    date_registered = models.DateTimeField(auto_now_add=True)
    exams = models.ManyToManyField("Exam", through="Student_on_Exam")
    authority = models.BooleanField(default=False, help_text="Makes and edits exams")

    def __str__(self):
        return f"""
            {self.student_id=}
            \t{self.date_registered=}
            \t{self.exams.count()=}
        """

class Exam(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    exam_name = models.CharField(max_length=256, unique=True)
    course_name = models.CharField(max_length=256)
    course_id = models.CharField(max_length=256)
    description = models.TextField(default="")
    exam_content = models.JSONField()
    answers = models.JSONField()
    attempts = models.SmallIntegerField(default=1)
    date_registered = models.DateTimeField(auto_now_add=True)
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    creator = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f"""
            {self.exam_name=}
            \t{self.course_name=}
            \t{self.course_id=}
            \t{self.date_registered=}
            \t{self.open_time=}
            \t{self.close_time=}
            """

    """
    exam_content example:
        
    {
        "exam":{
            "0":{
                "description":"Is the earth flat",
                "hint":"mafs",
                "qtype":"YN",
                "marks": 5
            },
            "1":{
                "description":"Which one of the following items isn't a fruit",
                "choices":[
                    "Apple",
                    "Orange",
                    "Table"
                ],
                "hint":"Everyday object",
                "qtype":"CO",
                "marks": 5
            },
            "2":{
                "description":"Which one of the following items is a fruit",
                "choices":[
                    "Apple",
                    "Orange",
                    "Table"
                ],
                "hint":"Plants",
                "qtype":"CM",
                "marks": 2
            },
            "3":{
                "description":"What is the language that dominates the web",
                "hint":"Plants",
                "qtype":"SA",
                "marks": 999
            }
        },
        "practice":{
            "0":{
                "description":"Does malloc zero?",
                "hint":"trying doesnt emsure the answer",
                "qtype":"YN"
            }
        }
    }


    answers example:
    {
        "exam":{
            "0":0,
            "1":2,
            "2":[
                0,
                1
            ],
            "3":"Javascript"
        },
        "practice":{
            "0":0
        }
    }
    """


def empty_dict():
    return {}

class Student_on_Exam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student_answers = models.JSONField(default=empty_dict)
    student_marks = models.DecimalField(max_digits=11, decimal_places=5, default=0)
    date_student_started = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_student_finished = models.DateTimeField(null=True, blank=True)

    def save(self, *arg, **kwargs):
        if self.date_student_finished is not None:
            self.student_marks = utilities.evaluate_answer(self.student_answers, self.exam.answers, self.exam.exam_content)
        super(Student_on_Exam, self).save(*arg, **kwargs)

    def __str__(self):
        return f"""
            {self.student.nickname=}
            \t{self.exam.exam_name=}
            \t{self.student_marks=}
            \t{self.date_student_started=}
            \t{self.date_student_finished=}
        """


def autofill_database():
    """Working 10% of the time :)"""
    from datetime import datetime, timedelta
    import json
    import random
    exam_str = """
{
        "exam":{
            "0":{
                "description":"Is the earth flat",
                "hint":"mafs",
                "qtype":"YN",
                "marks": 5
            },
            "1":{
                "description":"Which one of the following items isn't a fruit",
                "choices":[
                    "Apple",
                    "Orange",
                    "Table"
                ],
                "hint":"Everyday object",
                "qtype":"CO",
                "marks": 5
            },
            "2":{
                "description":"Which one of the following items is a fruit",
                "choices":[
                    "Apple",
                    "Orange",
                    "Table"
                ],
                "hint":"Plants",
                "qtype":"CM",
                "marks": 2
            },
            "3":{
                "description":"What is the language that dominates the web",
                "hint":"Plants",
                "qtype":"SA",
                "marks": 999
            }
        },
        "practice":{
            "0":{
                "description":"Does malloc zero?",
                "hint":"trying doesnt emsure the answer",
                "qtype":"YN"
            }
        }
    }    
    """
    solution_str = \
    """{
        "exam":{
            "0":0,
            "1":2,
            "2":[
                0,
                1
            ],
            "3":"Javascript"
        },
        "practice":{
            "0":0
        }
    }"""
    exam_content = json.loads(exam_str)
    solution = json.loads(solution_str)
    
    r1 = random.randint(100, 2000)
    s1 = Student.objects.create(
        student_id=r1, 
        nickname="Sample1", 
        date_registered=timezone.now(),
        user=User.objects.create(username=r1, password="pass"),
        authority=True
    )
    r2 = random.randint(100, 2000)
    s2 = Student.objects.create(
        student_id=r2, 
        nickname="Sample2",
        date_registered=timezone.now(),
        user=User.objects.create(username=r2, password="pass"),
        authority=True
    )
    x1 = Exam.objects.create(
        exam_name=str(randint(1000, 9000)),
        course_name="Crs1", 
        course_id="111", 
        exam_content=exam_content,
        answers=solution,
        attempts=2,
        description="First exam, hello world!",
        open_time=timezone.now(), 
        close_time=timezone.now() + timedelta(hours=1000), 
        creator=s1
    )
    x2 = Exam.objects.create(
        exam_name=str(randint(1000, 9000)),
        course_name="Crs2", 
        course_id="222", 
        exam_content=exam_content,
        answers=solution,
        attempts=50,
        description="Second exam, hello world!",
        open_time=timezone.now(), 
        close_time=timezone.now() + timedelta(hours=1000), 
        creator=s1
    )

    Student_on_Exam(
        student=s1, 
        exam=x1, 
        student_answers=solution,
        date_student_started=timezone.now(),
        date_student_finished=timezone.now() + timedelta(hours=0.8)
        ).save()
    Student_on_Exam(
        student=s2, 
        exam=x1, 
        student_answers=solution,
        date_student_started=timezone.now(),
        date_student_finished=timezone.now() + timedelta(hours=0.8)
        ).save()
