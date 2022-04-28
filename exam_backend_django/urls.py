"""exam_backend_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/setCSRFCookie', views.set_csrf_token),
    path('api/user/login', views.login_view),
    path('api/user/register', views.register_view),
    path('api/user/logout', views.logout_view),
    path('api/exam/getExams', views.get_exams_view),
    path('api/exam/getRanking', views.get_ranking_view),
    path('api/exam/getPastExams', views.get_past_exams_view),
    path('api/exam/getQuestions', views.get_questions_view),
    path('api/exam/submitAnswers', views.submit_answers_view),
    path('api/exam/deleteQuestion', views.delete_question_view),
    path('api/exam/addQuestion', views.add_question_view),
    # path('exam/getQuestions', views.get_questions),
    # path('exam/getQuestions', views.get_questions),
    # path('exam/getExams', views.get_exams_view),
    path('', views.hello_world_view),
]
