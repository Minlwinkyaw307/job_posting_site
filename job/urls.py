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
    path('faq/', faq, name='job.faq'),
    path('profile/', profile_index, name='job.profile_index'),
    path('profile/accepted-jobs', profile_accepted_jobs, name='job.profile_accepted_job'),
    path('profile/applied-jobs', profile_applied_jobs, name='job.profile_applied_job'),
    path('profile/rejected-jobs', profile_rejected_jobs, name='job.profile_rejected_job'),
    path('profile/saved-jobs', profile_saved_jobs, name='job.profile_saved_jobs'),
    path('profile/comments', profile_comments, name='job.profile_comments'),
    path('profile/change-password', profile_change_password, name='job.profile_change_password'),
    path('profile/change-profile', profile_change_profile, name='job.profile_change_profile'),
    path('profile/comments/<int:comment_id>/edit', profile_edit_comment, name='job.profile_edit_comment'),
    path('profile/comment/<int:comment_id>/delete', profile_delete_comment, name='job.profile_delete_comment'),
    path('profile/applications/<int:job_id>/delete', profile_delete_application, name='job.profile_delete_application'),
    path('profile/saved/applications/<int:job_id>/delete', profile_delete_saved_job, name='job.profile_delete_saved_job'),
    path('jobs/', jobs_view, name='job.jobs'),
    path('jobs/search/auto', jobs_search_job, name='job.auto_search_jobs'),
    path('job/detail/<str:slug>', job_detail, name='job.detail'),
    path('job/apply/<str:slug>', apply_job, name='job.apply'),
    path('job/save/<str:slug>', save_and_unsaved_job, name='job.save'),
]

