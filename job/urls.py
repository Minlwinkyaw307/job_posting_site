from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='job.index'),
    path('test/', test),
    path('login/', login_page, name='job.login_page'),
    path('signup/', signup_page, name='job.signup_page'),
    path('about/', about_view, name='job.about'),
    path('contact/', contact_us_view, name='job.contact_us'),
    path('jobs/', jobs_view, name='job.jobs'),
    path('job/detail/<str:slug>', job_detail, name='job.detail'),
    path('job/apply/<str:slug>', apply_job, name='job.apply'),
    path('job/save/<str:slug>', save_and_unsaved_job, name='job.save'),
]

