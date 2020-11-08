from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'index.html')


def VideosPage(request):
    print('here')
    return render(request, 'videos.html')
