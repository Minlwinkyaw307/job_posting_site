from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='job.index'),
    path('test/', test),
    path('login/', login_page, name='job.login_page'),
    path('job/detail/<str:slug>', job_detail, name='job.detail'),
]

