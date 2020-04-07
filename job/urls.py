from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='job.index'),
    path('test/', test),
    path('login/', login_page, name='job.login_page'),
    path('logout/', logout_view, name='job.logout'),
    path('signup/', signup_page, name='job.signup_page'),
    path('about/', about_view, name='job.about'),
    path('contact/', contact_us_view, name='job.contact_us'),
    path('profile/', profile_index, name='job.profile_index'),
    path('profile/accepted-jobs', profile_accepted_jobs, name='job.profile_accepted_job'),
    path('profile/applied-jobs', profile_applied_jobs, name='job.profile_applied_job'),
    path('profile/rejected-jobs', profile_rejected_jobs, name='job.profile_rejected_job'),
    path('profile/saved-jobs', profile_saved_jobs, name='job.profile_saved_jobs'),
    path('profile/applications/<int:job_id>/delete', profile_delete_application, name='job.profile_delete_application'),
    path('profile/saved/applications/<int:job_id>/delete', profile_delete_saved_job, name='job.profile_delete_saved_job'),
    path('jobs/', jobs_view, name='job.jobs'),
    path('job/detail/<str:slug>', job_detail, name='job.detail'),
    path('job/apply/<str:slug>', apply_job, name='job.apply'),
    path('job/save/<str:slug>', save_and_unsaved_job, name='job.save'),
]

