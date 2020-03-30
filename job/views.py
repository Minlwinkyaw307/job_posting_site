from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *

from .models import *
from setting.models import *


def index(request):
    # getting first setting
    setting = Setting.objects.all()[0]
    jobs = Job.objects.filter(status__id=1)
    print(jobs[0].image)
    data = {
        'title': "Index Title",
        'setting': setting,
        'jobs': jobs,
    }
    return render(request, 'job/index.html', data)


def test(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponse("Succeed")
    else:
        form = ImageForm()
    return render(request, 'job/test.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')
