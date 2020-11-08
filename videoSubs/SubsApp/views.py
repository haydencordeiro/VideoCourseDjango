from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
# Create your views here.


def home(request):
    freeVideos = Video.objects.filter(subType__name="Free")[0:10]
    context = {
        'freeVideos': freeVideos,
    }
    return render(request, 'index.html', context)


def VideosPage(request):
    print('here')
    return render(request, 'videos.html')
