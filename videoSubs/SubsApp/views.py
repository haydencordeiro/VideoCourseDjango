from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import logout
from django.contrib import messages
# Create your views here.


def home(request):

    # messages.info(request, 'Three credits remain in your account.')
    # messages.info(request, 'Three creditasdfs remain in your account.')

    # get list of first 10 free videos
    freeVideos = Video.objects.filter(subType__name="Free")[0:10]
    # get List of subscriptions
    accessList = []

    Sub_Type = SubType.objects.all()
    SubDetailsList = []
    for i in Sub_Type:
        SubDetailsList.append(
            [i,
             str(len(Video.objects.filter(subType=i)))+" "+i.name+" Videos"])
        temp = TypeAccess.objects.filter(
            subType=i)
        temp2 = [i.canAccess.name for i in temp]
        accessList.append(','.join(temp2))
    SubDetailsList.append(['', '24 hours access'])
    print(SubDetailsList, accessList)
    context = {
        'freeVideos': freeVideos,
        'SubDetailsList': SubDetailsList,
        'Sub_Type': zip(Sub_Type, accessList),
    }
    return render(request, 'index.html', context)


def VideosPage(request):
    print('here')
    return render(request, 'videos.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
