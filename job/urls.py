from .views import *
from django.urls import path

urlpatterns = [
    path('test/', test),
    path('', index, name='job.index'),
]

