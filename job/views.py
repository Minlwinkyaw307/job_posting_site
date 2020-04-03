from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


from .forms import *

from .models import *
from setting.models import *


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
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponse("Succeed")
    else:
        form = ImageForm()
    return render(request, 'job/test.html', {'form': form})


def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    setting = Setting.objects.all()[0]
    context = {
        'job': job,
        'title': "Index Title",
        'setting': setting,
    }
    return render(request, 'job/job_detail.html', context)


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


