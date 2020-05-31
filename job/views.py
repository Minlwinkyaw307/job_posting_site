import json

from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import constants
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from .forms import *
from setting.forms import *
from .models import *
from setting.models import *


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')


def index(request):
    # getting first setting
    setting = Setting.objects.all()[0]
    jobs = Job.objects.filter(status=True)

    context = {
        'title': "Index Title",
        'setting': setting,
        'jobs': jobs,
    }
    return render(request, 'job/index.html', context)


def test(request):
    # if request.method == 'POST':
    #     form = ImageForm(request.POST, request.FILES)
    #
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponse("Succeed")
    # else:
    #     form = ImageForm()
    return render(request, 'job/test.html')


def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        comment = Comment(ip=get_ip(request), user=customer, job=job)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('job.detail', slug=slug)
    else:
        form = CommentForm(request.POST)
    if request.user.is_authenticated:
        applied = Application.objects.filter(applicant=request.user, job=job).count()
        saved = Saved.objects.filter(applicant=request.user, job=job).count()
    else:
        applied = False
        saved = False
    setting = Setting.objects.all()[0]
    context = {
        'job': job,
        'title': "Index Title",
        'setting': setting,
        'applied': bool(applied),
        'saved': bool(saved),
        'form': form,
        'comments': Comment.objects.filter(job=job),
    }
    print(job.images)
    return render(request, 'job/job_detail.html', context)


@login_required(login_url='/login')
def apply_job(request, slug):
    job = get_object_or_404(Job, slug=slug)
    # job = Job.objects.get(slug=slug)
    applied = Application.objects.filter(applicant=request.user, job=job).count()
    if applied == 0:
        ip = get_ip(request)
        Application(job=job, applicant=request.user, ip=ip).save()
        messages.add_message(request, messages.SUCCESS, 'Successfully Applied.')
    else:
        messages.add_message(request, messages.ERROR, 'You Have Already Applied This Job.')
    return redirect('job.detail', slug=slug)


@login_required(login_url='/login')
def save_and_unsaved_job(request, slug):
    job = get_object_or_404(Job, slug=slug)
    saved = Saved.objects.filter(applicant=request.user, job=job)
    if len(saved) == 0:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        Saved(job=job, applicant=request.user, ip=ip).save()
        messages.add_message(request, messages.SUCCESS, 'Successfully Saved.')
    else:
        saved.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully Unsaved')
    return redirect('job.detail', slug=slug)


def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        return redirect('job.index')
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['email']
        password = request.POST['password']
        user: User = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin:index')
                return redirect('job.index')
            else:
                messages.add_message(request, messages.ERROR, 'Your account was inactive.')
                return render(request, 'job/login.html')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Email or Password')
            return render(request, 'job/login.html')

    context = {
        'title': "Index Title",
    }
    return render(request, 'job/login.html', context)


def signup_page(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            # TODO: delete 2 lines
            user.is_superuser = True
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('job.index')
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    else:
        form = SignUpForm(data=request.POST)
        print("Not POST")
    context = {
        'title': "Page Title",
        'form': form
    }
    return render(request, 'job/signup.html', context)


def jobs_view(request):
    q = request.GET['q'] if request.GET.__contains__('q') else ''
    city = request.GET['city'] if request.GET.__contains__('city') else ''
    job_type = request.GET['type'] if request.GET.__contains__('type') else ''
    category = request.GET['category'] if request.GET.__contains__('category') else ''
    jobs = Job.objects.filter(Q(status=True) & ((Q(title__contains=q) | Q(company_name__contains=q)) &
                                                (Q(city__name__contains=city) & Q(job_type__contains=job_type)) &
                                                Q(category__title__contains=category)))
    cities = City.objects.all()
    categories = Category.objects.filter(parent=None, status=True)
    context = {
        'title': 'Jobs',
        'jobs': jobs,
        'cities': cities,
        'categories': categories,
    }
    return render(request, 'job/jobs.html', context)


def jobs_search_job(request):
    q = request.GET['q'] if request.GET.__contains__('q') else ''
    city = request.GET['city'] if request.GET.__contains__('city') else ''
    job_type = request.GET['type'] if request.GET.__contains__('type') else ''
    category = request.GET['category'] if request.GET.__contains__('category') else ''
    jobs = Job.objects.filter(Q(status=True) & ((Q(title__contains=q) | Q(company_name__contains=q)) &
                                                (Q(city__name__contains=city) & Q(
                                                    job_type__contains=job_type)) &
                                                Q(category__title__contains=category)))
    result = {}
    for job in jobs:
        result[job.slug] = job.title
    mimeType = 'application/json'
    return HttpResponse(json.dumps(result), mimeType)


def about_view(request):
    setting = Setting.objects.all()[0]
    users = User.objects.all().count()
    jobs = Job.objects.all().count()
    applications = Application.objects.all().count()
    context = {
        'title': 'Jobs',
        'setting': setting,
        'users': users,
        'jobs': jobs,
        'applications': applications,
    }
    return render(request, 'job/about.html', context)


def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            message.ip = get_ip(request)
            message.save()
            messages.add_message(request, messages.SUCCESS, "Successfully Submitted.")
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    form = ContactForm()
    setting = Setting.objects.all()[0]
    context = {
        'title': 'Jobs',
        'setting': setting,
        'form': form,
    }
    return render(request, 'job/contact-us.html', context)


@login_required(login_url='/login')
def profile_index(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        profile_user_update_form = ProfileUserUpdateForm(request.POST, instance=request.user)
        profile_form = CustomerProfileUpdateForm(request.POST, instance=customer)
        if profile_user_update_form.is_valid() and profile_form.is_valid():
            profile_user_update_form.save()
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully Updated')
            return redirect('job.profile_index')
        else:
            messages.add_message(request, messages.ERROR, profile_user_update_form.errors)
            return redirect('job.profile_index')
    setting = Setting.objects.all()[0]
    profile_user_update_form = ProfileUserUpdateForm(instance=request.user)
    profile_form = CustomerProfileUpdateForm(instance=customer)
    context = {
        'title': 'Jobs',
        'customer': customer,
        'setting': setting,
        'page': 'profile',
        'profile_user_update_form': profile_user_update_form,
        'profile_form': profile_form,
    }
    return render(request, 'job/profile_index.html', context)


@login_required(login_url='/login')
def profile_accepted_jobs(request):
    customer = Customer.objects.get(user=request.user)
    accepted_jobs = Application.objects.filter(applicant=request.user, status='Accepted')
    setting = Setting.objects.all()[0]
    context = {
        'title': 'Jobs',
        'customer': customer,
        'setting': setting,
        'page': 'accepted_jobs',
        'applications': accepted_jobs,
    }
    return render(request, 'job/profile_accepted_jobs.html', context)


@login_required(login_url='/login')
def profile_applied_jobs(request):
    customer = Customer.objects.get(user=request.user)
    applied_jobs = Application.objects.filter(applicant=request.user)
    setting = Setting.objects.all()[0]
    context = {
        'title': 'Jobs',
        'customer': customer,
        'setting': setting,
        'page': 'applied_jobs',
        'applications': applied_jobs,
    }
    return render(request, 'job/profile_applied_jobs.html', context)


@login_required(login_url='/login')
def profile_rejected_jobs(request):
    customer = Customer.objects.get(user=request.user)
    rejected_jobs = Application.objects.filter(applicant=request.user, status='Rejected')
    setting = Setting.objects.all()[0]
    context = {
        'title': 'Jobs',
        'customer': customer,
        'setting': setting,
        'page': 'rejected_jobs',
        'applications': rejected_jobs,
    }
    return render(request, 'job/profile_rejected_jobs.html', context)


@login_required(login_url='/login')
def profile_saved_jobs(request):
    customer = Customer.objects.get(user=request.user)
    saved_jobs = Saved.objects.filter(applicant=request.user)
    setting = Setting.objects.all()[0]
    context = {
        'title': 'Jobs',
        'customer': customer,
        'setting': setting,
        'page': 'saved_jobs',
        'applications': saved_jobs,
    }
    return render(request, 'job/profile_saved_jobs.html', context)


@login_required(login_url='/login')
def profile_comments(request):
    customer = Customer.objects.get(user=request.user)
    comments = Comment.objects.filter(user__user=request.user)
    setting = Setting.objects.all()[0]
    context = {
        'title': 'Jobs',
        'customer': customer,
        'setting': setting,
        'page': 'comments',
        'comments': comments,
    }
    return render(request, 'job/profile_comments.html', context)


@login_required(login_url='/login')
def profile_delete_application(request, job_id):
    Application.objects.get(id=job_id).delete()
    return HttpResponseRedirect(request.GET['path'])


@login_required(login_url='/login')
def profile_delete_saved_job(request, job_id):
    Saved.objects.get(id=job_id).delete()
    return HttpResponseRedirect(request.GET['path'])


@login_required(login_url='/login')
def profile_delete_comment(request, comment_id):
    Comment.objects.get(id=comment_id).delete()
    return HttpResponseRedirect(request.GET['path'])


@login_required(login_url='/login')
def profile_edit_comment(request, comment_id):
    customer = Customer.objects.get(user=request.user)
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.updated_at = timezone.now()
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('job.profile_comments')
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return redirect('job.profile_edit_comment', comment_id=comment_id)
    else:
        form = CommentForm(instance=comment)
    setting = Setting.objects.all()[0]
    context = {
        'title': 'Jobs',
        'customer': customer,
        'setting': setting,
        'page': 'comments',
        'form': form,
    }
    return render(request, 'job/profile_edit_comment.html', context)


@login_required(login_url='/login')
def profile_change_password(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Your password was successfully updated!')
            return redirect('job.profile_change_password')
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return redirect('job.profile_change_password')
    else:
        form = PasswordChangeForm(request.user)

    setting = Setting.objects.all()[0]
    context = {
        'title': 'Jobs',
        'customer': customer,
        'setting': setting,
        'page': 'change_password',
        'form': form,
    }
    return render(request, 'job/profile_change_password.html', context)


@login_required(login_url='/login')
def profile_change_profile(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST or None, request.FILES or None, instance=customer)
        if form.is_valid():
            cust = form.save()
            messages.add_message(request, messages.SUCCESS, 'Your Profile was successfully updated!')
            return redirect('job.profile_change_profile')
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return redirect('job.profile_change_profile')
    else:
        form = ChangeProfileForm(instance=request.user)
    setting = Setting.objects.all()[0]
    context = {
        'title': 'Jobs',
        'customer': customer,
        'setting': setting,
        'page': 'change_profile',
        'form': form,
    }
    return render(request, 'job/profile_change_profile.html', context)


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('job.login_page')


def faq(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Successfully Sent.")
            return redirect('job.faq')
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    setting = Setting.objects.all()[0]
    form = FAQForm(request.POST)
    faqs = FAQ.objects.filter(status='Answered')
    context = {
        'title': 'Jobs',
        'setting': setting,
        'form': form,
        'faqs': faqs,
    }
    return render(request, 'job/faq.html', context)
