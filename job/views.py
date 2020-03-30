from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *


# Create your views here.
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